# Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT REQUEST                           │
│                    POST /analyze {idea}                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│                         (main.py)                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator                            │
│                   (orchestrator.py)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  RAG System  │    │  Web Search  │    │  LLM (Groq)  │
│              │    │              │    │              │
│ - Embeddings │    │ DuckDuckGo   │    │ Llama3-70B   │
│ - Retrieval  │    │ Search       │    │              │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Pipeline                          │
│                                                                  │
│  1. Planner Agent          ─→  Strategic planning + web search  │
│  2. Market Analysis Agent  ─→  Market size, trends, gaps        │
│  3. Target Audience Agent  ─→  Customer segmentation            │
│  4. Competition Agent      ─→  Competitive landscape            │
│  5. Revenue Agent          ─→  Revenue model design             │
│  6. Cost Agent             ─→  Cost structure analysis          │
│  7. GTM Agent              ─→  Go-to-market strategy            │
│  8. Success Agent          ─→  Success probability + location   │
│  9. Critic Agent           ─→  Quality review & improvements    │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Structured JSON Report                         │
│                                                                  │
│  {                                                               │
│    market_analysis: "...",                                       │
│    target_audience: "...",                                       │
│    revenue_model: "...",                                         │
│    competition_analysis: "...",                                  │
│    cost_structure: "...",                                        │
│    go_to_market: "...",                                          │
│    success_probability: 72.5,                                    │
│    best_location: "San Francisco, CA"                            │
│  }                                                               │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Store in DB  │    │ Return to    │    │ Generate     │
│              │    │ Client       │    │ Critique     │
│ Vector DB    │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Data Flow

```
Request → Validation → RAG Retrieval → Web Search → Agent Pipeline → Response
                           ↓                            ↓
                    Similar Ideas                  Store Report
                           ↓                            ↓
                    Vector Database ←────────────────────┘
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────────┐
│                         COMPONENTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │   FastAPI    │────────▶│ Orchestrator │                     │
│  │  Endpoints   │         │              │                     │
│  └──────────────┘         └──────┬───────┘                     │
│                                   │                              │
│  ┌──────────────┐         ┌──────▼───────┐                     │
│  │   Pydantic   │────────▶│    Agents    │                     │
│  │   Schemas    │         │   (8 types)  │                     │
│  └──────────────┘         └──────┬───────┘                     │
│                                   │                              │
│  ┌──────────────┐         ┌──────▼───────┐                     │
│  │     RAG      │◀────────│   Groq LLM   │                     │
│  │  Embeddings  │         │   Llama3     │                     │
│  └──────┬───────┘         └──────────────┘                     │
│         │                                                        │
│  ┌──────▼───────┐         ┌──────────────┐                     │
│  │   Vector DB  │         │  Web Search  │                     │
│  │  (pgvector)  │         │ (DuckDuckGo) │                     │
│  └──────────────┘         └──────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Workflow

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│ 1. Retrieve Similar Ideas   │ ◀── RAG System
│    (Vector Similarity)      │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 2. Planner Agent            │ ◀── Web Search
│    - Create strategy        │
│    - Search market trends   │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 3. Market Analysis Agent    │ ◀── LLM
│    - Market size & trends   │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 4. Target Audience Agent    │ ◀── LLM
│    - Customer segments      │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 5. Competition Agent        │ ◀── LLM
│    - Competitive analysis   │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 6. Revenue Agent            │ ◀── LLM
│    - Revenue model          │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 7. Cost Agent               │ ◀── LLM
│    - Cost structure         │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 8. GTM Agent                │ ◀── LLM
│    - Go-to-market strategy  │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 9. Success Agent            │ ◀── LLM
│    - Probability score      │
│    - Best location          │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 10. Critic Agent            │ ◀── LLM
│     - Review report         │
│     - Identify weaknesses   │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│ 11. Store Report            │ ──▶ Vector DB
│     (with embeddings)       │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────┐
│   RETURN    │
│   REPORT    │
└─────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY LAYERS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  API Layer:          FastAPI + Uvicorn                          │
│                                                                  │
│  Validation:         Pydantic                                   │
│                                                                  │
│  AI/LLM:             Groq (Llama3-70B) via LangChain           │
│                                                                  │
│  Embeddings:         HuggingFace sentence-transformers          │
│                      (all-MiniLM-L6-v2)                         │
│                                                                  │
│  Vector DB:          Supabase PostgreSQL + pgvector             │
│                                                                  │
│  Web Search:         DuckDuckGo via LangChain                   │
│                                                                  │
│  Orchestration:      Custom multi-agent system                  │
│                                                                  │
│  Deployment:         Docker + Docker Compose                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Database Schema

```
┌─────────────────────────────────────────────────────────────────┐
│                    startup_ideas Table                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  id              SERIAL PRIMARY KEY                              │
│  idea            TEXT NOT NULL                                   │
│  embedding       vector(384)                                     │
│  report          JSONB                                           │
│  created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP            │
│  updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP            │
│                                                                  │
│  INDEX: startup_ideas_embedding_idx (IVFFlat, cosine)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION DEPLOYMENT                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │   Client     │────────▶│ Load Balancer│                     │
│  │  (Browser)   │         │              │                     │
│  └──────────────┘         └──────┬───────┘                     │
│                                   │                              │
│                          ┌────────┴────────┐                    │
│                          │                 │                    │
│                   ┌──────▼───────┐  ┌──────▼───────┐           │
│                   │  API Server  │  │  API Server  │           │
│                   │  (Docker)    │  │  (Docker)    │           │
│                   └──────┬───────┘  └──────┬───────┘           │
│                          │                 │                    │
│                          └────────┬────────┘                    │
│                                   │                              │
│                          ┌────────▼────────┐                    │
│                          │                 │                    │
│                   ┌──────▼───────┐  ┌──────▼───────┐           │
│                   │  Supabase    │  │  Groq API    │           │
│                   │  PostgreSQL  │  │  (LLM)       │           │
│                   │  + pgvector  │  │              │           │
│                   └──────────────┘  └──────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Legend:**
- `─→` Sequential flow
- `◀──` Data source
- `│` Connection
- `▼` Next step
