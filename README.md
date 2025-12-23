# Content Search Backend

Content Search Backend is a production-oriented FastAPI service that provides
ML-powered semantic search over business content using vector embeddings.

The system abstracts away machine learning models, vector similarity logic,
and database complexity behind clean, secure APIs, enabling frontend or CMS
applications to retrieve semantically relevant content without managing
embeddings or search infrastructure directly.

## Key Features

- **Semantic Search with pgvector**
  - Content is embedded into fixed-length vectors (1536-dim)
  - Similarity search is performed directly inside PostgreSQL using pgvector
  - Supports top-K nearest neighbor retrieval via L2 distance or inner product

- **PostgreSQL + Supabase**
  - Supabase-hosted PostgreSQL as the primary datastore
  - pgvector extension enabled for native vector search
  - Standard relational data and vector data stored together

- **Authentication & Authorization**
  - Supabase Auth (JWT-based)
  - Protected endpoints for content creation and semantic search
  - Public endpoints for health checks and debugging

- **Clean API Design**
  - RESTful endpoints for content ingestion and retrieval
  - Pydantic schemas for request/response validation
  - Centralized error handling and logging

## API Overview

| Endpoint | Method | Auth | Description |
|--------|------|------|------------|
| `/health` | GET | ❌ | Service health check |
| `/analyze` | POST | ❌ | Debug endpoint (no DB write) |
| `/contents` | POST | ✅ | Create content with embedding |
| `/contents/{id}` | GET | ❌ | Retrieve content by ID |
| `/search` | POST | ✅ | Semantic vector search |

## Project Goal

This project is designed as a **realistic backend foundation** for:

- AI-powered content platforms
- Internal enterprise search systems
- RAG-style applications
- CMS or knowledge-base search services

The architecture intentionally mirrors how modern production systems
(OpenAI, Notion, Perplexity-style stacks) integrate vector search
into traditional databases.
