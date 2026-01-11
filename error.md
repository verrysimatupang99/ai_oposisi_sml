PS C:\\Coding\\ai\_oposisi\_sml> cd backend

PS C:\\Coding\\ai\_oposisi\_sml\\backend> .\\venv\\scripts\\activate

(venv) PS C:\\Coding\\ai\_oposisi\_sml\\backend> uvicorn app.main:app --reload

INFO:     Will watch for changes in these directories: \['C:\\\\Coding\\\\ai\_oposisi\_sml\\\\backend']

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

INFO:     Started reloader process \[11784] using WatchFiles

2026-01-12 01:34:25,282 - root - INFO - Logging configuration loaded successfully

2026-01-12 01:34:25,327 - uvicorn.error - INFO - Started server process \[21468]

2026-01-12 01:34:25,328 - uvicorn.error - INFO - Waiting for application startup.

2026-01-12 01:34:25,330 - app.main - INFO - 🚀 Starting AI Tokoh Oposisi \& Intelektual Kritis application...

2026-01-12 01:34:25,332 - app.main - INFO - 🗄️  Initializing database...

2026-01-12 01:34:25,333 - app.core.database - INFO - 🗄️  Creating database tables...

2026-01-12 01:34:25,358 - app.core.database - INFO - ✅ Database tables created successfully

2026-01-12 01:34:25,360 - app.main - INFO - ✅ Database initialized successfully

2026-01-12 01:34:25,361 - app.main - INFO - 🤖 Initializing AI services...

2026-01-12 01:34:25,362 - app.services.llm\_service - INFO - 🤖 Initializing LLM service...

2026-01-12 01:34:26,392 - httpx - INFO - HTTP Request: GET http://localhost:1234/v1/models "HTTP/1.1 200 OK"

2026-01-12 01:34:26,394 - app.services.llm\_service - WARNING - ⚠️  LLM Studio not available: LM Studio test failed: Model llama-2-7b-chat not available. Available models: \['meta-llama-3-8b-instruct-bpe-fix', 'text-embedding-nomic-embed-text-v1.5', 'llama-3.2-1b-instruct']

2026-01-12 01:34:26,395 - app.services.llm\_service - INFO - 📝 Running in MOCK mode - LLM requests will return mock responses

2026-01-12 01:34:26,395 - app.main - INFO - ✅ LLM service initialized

2026-01-12 01:34:26,396 - app.services.persona\_service - INFO - 🎭 Initializing Persona service...

2026-01-12 01:34:26,397 - app.services.persona\_service - INFO - ✅ Loaded 1 default personas

2026-01-12 01:34:26,397 - app.services.persona\_service - INFO - ✅ Persona service initialized successfully

2026-01-12 01:34:26,398 - app.main - INFO - ✅ Persona service initialized

2026-01-12 01:34:26,399 - app.services.ethics\_service - INFO - 🛡️  Initializing Ethics service...

2026-01-12 01:34:26,399 - app.services.ethics\_service - INFO - ✅ Ethics service initialized successfully

2026-01-12 01:34:26,400 - app.main - INFO - ✅ Ethics service initialized

2026-01-12 01:34:26,400 - app.main - INFO - 🎉 All services initialized successfully

2026-01-12 01:34:26,401 - uvicorn.error - INFO - Application startup complete.



