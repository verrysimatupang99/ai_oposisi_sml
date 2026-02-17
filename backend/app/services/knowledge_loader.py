"""
Knowledge Base Loader

Utilities for loading and chunking documents from the knowledge base
directory into the RAG system.

Author: AI Assistant
Created: 2026-01-13
"""

import logging
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)


class DocumentChunker:
    """
    Splits documents into smaller chunks for embedding.
    Uses semantic chunking based on paragraphs and headers.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Full document text
            metadata: Base metadata to include with each chunk
            
        Returns:
            List of chunk dicts with 'content' and 'metadata'
        """
        metadata = metadata or {}
        chunks = []
        
        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text.strip())
        
        current_chunk = ""
        chunk_index = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # If adding this paragraph exceeds chunk size
            if len(current_chunk) + len(para) > self.chunk_size:
                # Save current chunk if big enough
                if len(current_chunk) >= self.min_chunk_size:
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": {
                            **metadata,
                            "chunk_index": chunk_index
                        }
                    })
                    chunk_index += 1
                
                # Start new chunk with overlap
                if self.chunk_overlap > 0 and current_chunk:
                    # Take last N chars as overlap
                    overlap = current_chunk[-self.chunk_overlap:]
                    current_chunk = overlap + "\n\n" + para
                else:
                    current_chunk = para
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
        
        # Don't forget the last chunk
        if len(current_chunk) >= self.min_chunk_size:
            chunks.append({
                "content": current_chunk.strip(),
                "metadata": {
                    **metadata,
                    "chunk_index": chunk_index
                }
            })
        
        return chunks


class KnowledgeLoader:
    """
    Loads documents from the knowledge base directory.
    Supports markdown and text files.
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or settings.KNOWLEDGE_BASE_PATH)
        self.chunker = DocumentChunker()
        self.logger = logging.getLogger(f"{__name__}.KnowledgeLoader")
    
    def _extract_metadata_from_markdown(self, content: str, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from markdown frontmatter or content.
        
        Args:
            content: File content
            file_path: Path to file
            
        Returns:
            Metadata dict
        """
        metadata = {
            "source": file_path.name,
            "file_path": str(file_path),
            "loaded_at": datetime.now().isoformat()
        }
        
        # Try to extract YAML frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        # Extract title from first H1
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match and "title" not in metadata:
            metadata["title"] = title_match.group(1).strip()
        
        # Infer topic from path
        if file_path.parent.name != self.base_path.name:
            metadata["topic"] = file_path.parent.name
        
        return metadata
    
    def _clean_markdown(self, content: str) -> str:
        """
        Remove frontmatter and clean markdown for embedding.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Cleaned text
        """
        # Remove YAML frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        
        # Convert headers to plain text with emphasis
        content = re.sub(r'^#{1,6}\s+(.+)$', r'\1:', content, flags=re.MULTILINE)
        
        # Remove markdown links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        
        # Remove bold/italic markers
        content = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', content)
        content = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', content)
        
        # Clean up extra whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()
    
    def load_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load and chunk a single file.
        
        Args:
            file_path: Path to file
            
        Returns:
            List of document chunks
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Extract metadata
            metadata = self._extract_metadata_from_markdown(content, file_path)
            
            # Clean content
            clean_content = self._clean_markdown(content)
            
            # Chunk the content
            chunks = self.chunker.chunk_text(clean_content, metadata)
            
            self.logger.info(f"Loaded {file_path.name}: {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            self.logger.error(f"Failed to load {file_path}: {e}")
            return []
    
    def load_directory(self, subdir: str = None) -> List[Dict[str, Any]]:
        """
        Load all documents from a directory.
        
        Args:
            subdir: Optional subdirectory (e.g., 'politics', 'figures')
            
        Returns:
            List of all document chunks
        """
        search_path = self.base_path / subdir if subdir else self.base_path
        
        if not search_path.exists():
            self.logger.warning(f"Directory not found: {search_path}")
            return []
        
        all_chunks = []
        
        # Find all markdown and text files
        for pattern in ['**/*.md', '**/*.txt']:
            for file_path in search_path.glob(pattern):
                chunks = self.load_file(file_path)
                all_chunks.extend(chunks)
        
        self.logger.info(f"Loaded {len(all_chunks)} total chunks from {search_path}")
        return all_chunks
    
    def load_all(self) -> List[Dict[str, Any]]:
        """
        Load all documents from the entire knowledge base.
        
        Returns:
            List of all document chunks
        """
        return self.load_directory()


async def ingest_knowledge_base(rag_service) -> int:
    """
    Convenience function to ingest the entire knowledge base into RAG.
    
    Args:
        rag_service: Initialized RAGService instance
        
    Returns:
        Number of documents ingested
    """
    loader = KnowledgeLoader()
    chunks = loader.load_all()
    
    if chunks:
        doc_ids = await rag_service.add_documents(chunks)
        logger.info(f"Ingested {len(doc_ids)} chunks into RAG")
        return len(doc_ids)
    
    return 0
