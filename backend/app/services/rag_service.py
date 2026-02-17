"""
RAG (Retrieval Augmented Generation) Service

This module implements RAG to ground AI responses with factual context
from a knowledge base, reducing hallucinations.

Author: AI Assistant
Created: 2026-01-13
"""

import logging
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

import httpx
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Represents a document chunk with metadata."""
    content: str
    metadata: Dict[str, Any]
    doc_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.doc_id:
            # Generate unique ID from content hash
            self.doc_id = hashlib.md5(self.content.encode()).hexdigest()[:16]


@dataclass
class RetrievalResult:
    """Result from vector search."""
    document: Document
    score: float
    

class EmbeddingService:
    """
    Service for generating text embeddings via LM Studio.
    Uses the embedding endpoint at /v1/embeddings.
    """
    
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or settings.LM_STUDIO_URL
        self.model = model or getattr(settings, 'EMBEDDING_MODEL', 'text-embedding-nomic-embed-text-v1.5')
        self.client: Optional[httpx.AsyncClient] = None
        self.logger = logging.getLogger(f"{__name__}.EmbeddingService")
    
    async def initialize(self):
        """Initialize HTTP client for embedding requests."""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0
        )
        self.logger.info(f"EmbeddingService initialized: {self.base_url}, model: {self.model}")
    
    async def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        return (await self.embed_batch([text]))[0]
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not self.client:
            await self.initialize()
        
        try:
            response = await self.client.post(
                "/v1/embeddings",
                json={
                    "model": self.model,
                    "input": texts
                }
            )
            response.raise_for_status()
            
            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Embedding failed: {e}")
            raise
    
    async def cleanup(self):
        """Close HTTP client."""
        if self.client:
            await self.client.aclose()


class VectorStore:
    """
    ChromaDB-based vector store for document embeddings.
    Handles persistence and semantic search.
    """
    
    def __init__(
        self,
        collection_name: str = "knowledge_base",
        persist_directory: str = None
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory or str(
            Path(settings.KNOWLEDGE_BASE_PATH) / "chroma_db"
        )
        self.client: Optional[chromadb.ClientAPI] = None
        self.collection = None
        self.logger = logging.getLogger(f"{__name__}.VectorStore")
    
    def initialize(self):
        """Initialize ChromaDB client and collection."""
        # Create persist directory if not exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "AI Oposisi Knowledge Base"}
        )
        
        self.logger.info(
            f"VectorStore initialized: {self.persist_directory}, "
            f"collection: {self.collection_name}, "
            f"documents: {self.collection.count()}"
        )
    
    def add_documents(
        self,
        documents: List[Document],
        embeddings: List[List[float]]
    ):
        """
        Add documents with their embeddings to the store.
        
        Args:
            documents: List of Document objects
            embeddings: Corresponding embedding vectors
        """
        if not self.collection:
            self.initialize()
        
        self.collection.add(
            ids=[doc.doc_id for doc in documents],
            embeddings=embeddings,
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents]
        )
        
        self.logger.info(f"Added {len(documents)} documents to vector store")
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        min_score: float = 0.0
    ) -> List[RetrievalResult]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            min_score: Minimum similarity score (0-1)
            
        Returns:
            List of RetrievalResult objects
        """
        if not self.collection:
            self.initialize()
        
        if self.collection.count() == 0:
            return []
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )
        
        retrieval_results = []
        
        for i, (doc_content, metadata, distance) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            # ChromaDB returns L2 distance, convert to similarity score
            # Lower distance = higher similarity
            score = 1.0 / (1.0 + distance)
            
            if score >= min_score:
                retrieval_results.append(RetrievalResult(
                    document=Document(
                        content=doc_content,
                        metadata=metadata,
                        doc_id=results["ids"][0][i]
                    ),
                    score=score
                ))
        
        return retrieval_results
    
    def count(self) -> int:
        """Get total number of documents in store."""
        if not self.collection:
            self.initialize()
        return self.collection.count()
    
    def clear(self):
        """Delete all documents from the collection."""
        if self.client and self.collection:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            self.logger.info("Vector store cleared")


class RAGService:
    """
    Main RAG orchestration service.
    Coordinates embedding, retrieval, and context building.
    """
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.is_initialized = False
        self.logger = logging.getLogger(f"{__name__}.RAGService")
        
        # Configuration
        self.top_k = getattr(settings, 'RAG_TOP_K', 3)
        self.min_score = getattr(settings, 'RAG_SIMILARITY_THRESHOLD', 0.3)
    
    async def initialize(self):
        """Initialize RAG components."""
        try:
            self.logger.info("Initializing RAG service...")
            
            # Initialize embedding service
            await self.embedding_service.initialize()
            
            # Initialize vector store
            self.vector_store.initialize()
            
            self.is_initialized = True
            self.logger.info(
                f"RAG service initialized. "
                f"Knowledge base contains {self.vector_store.count()} documents."
            )
            
        except Exception as e:
            self.logger.error(f"Failed to initialize RAG service: {e}")
            self.is_initialized = False
    
    async def add_document(
        self,
        content: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Add a single document to the knowledge base.
        
        Args:
            content: Document text
            metadata: Optional metadata (source, date, topic, etc.)
            
        Returns:
            Document ID
        """
        doc = Document(content=content, metadata=metadata or {})
        embedding = await self.embedding_service.embed(content)
        self.vector_store.add_documents([doc], [embedding])
        return doc.doc_id
    
    async def add_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Add multiple documents to the knowledge base.
        
        Args:
            documents: List of dicts with 'content' and optional 'metadata'
            
        Returns:
            List of document IDs
        """
        docs = [
            Document(
                content=d["content"],
                metadata=d.get("metadata", {})
            )
            for d in documents
        ]
        
        # Batch embed
        texts = [d.content for d in docs]
        embeddings = await self.embedding_service.embed_batch(texts)
        
        self.vector_store.add_documents(docs, embeddings)
        
        return [d.doc_id for d in docs]
    
    async def retrieve(
        self,
        query: str,
        top_k: int = None
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: User question/query
            top_k: Number of results (defaults to config)
            
        Returns:
            List of relevant documents with scores
        """
        if not self.is_initialized:
            self.logger.warning("RAG service not initialized, returning empty results")
            return []
        
        try:
            # Embed query
            query_embedding = await self.embedding_service.embed(query)
            
            # Search vector store
            results = self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k or self.top_k,
                min_score=self.min_score
            )
            
            self.logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            self.logger.error(f"Retrieval failed: {e}")
            return []
    
    def build_context(self, results: List[RetrievalResult]) -> str:
        """
        Build context string from retrieval results.
        
        Args:
            results: List of RetrievalResult objects
            
        Returns:
            Formatted context string for LLM prompt
        """
        if not results:
            return ""
        
        context_parts = ["=== KONTEKS FAKTUAL ===\n"]
        
        for i, result in enumerate(results, 1):
            source = result.document.metadata.get("source", "Unknown")
            date = result.document.metadata.get("date", "")
            
            context_parts.append(
                f"[{i}] Sumber: {source}"
                + (f" ({date})" if date else "")
                + f"\n{result.document.content}\n"
            )
        
        context_parts.append(
            "\n=== INSTRUKSI ===\n"
            "Gunakan konteks faktual di atas untuk menjawab pertanyaan. "
            "Jika informasi tidak tersedia dalam konteks, katakan bahwa "
            "Anda tidak memiliki informasi terkini tentang topik tersebut. "
            "Selalu sebutkan sumber jika mengutip fakta.\n"
        )
        
        return "\n".join(context_parts)
    
    async def get_augmented_context(self, query: str) -> str:
        """
        Get augmented context for a query (convenience method).
        
        Args:
            query: User question
            
        Returns:
            Context string ready to append to system prompt
        """
        results = await self.retrieve(query)
        return self.build_context(results)
    
    async def cleanup(self):
        """Cleanup resources."""
        await self.embedding_service.cleanup()


# Global instance
rag_service = RAGService()
