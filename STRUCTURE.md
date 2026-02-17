# Project Structure

```
ST Engine/
│
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── package.json                     # Project metadata
├── Dockerfile                       # Docker container configuration
├── docker-compose.yml              # Docker Compose configuration
│
├── README.md                        # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── DEPLOYMENT.md                   # Deployment guide
├── STRUCTURE.md                    # This file
│
├── agents/                         # Multi-agent system
│   ├── __init__.py
│   ├── base_agent.py              # Base agent class with LLM
│   ├── planner_agent.py           # Planning & web search
│   ├── analysis_agents.py         # Market, competition, revenue
│   ├── strategy_agents.py         # Cost, GTM, target audience
│   ├── evaluation_agents.py       # Success probability & critic
│   └── orchestrator.py            # Agent workflow coordinator
│
├── rag/                           # RAG implementation
│   ├── __init__.py
│   ├── embeddings.py              # HuggingFace sentence-transformers
│   └── retrieval.py               # Vector search & context building
│
├── tools/                         # External tools
│   ├── __init__.py
│   └── web_search.py              # DuckDuckGo search integration
│
├── models/                        # Data models
│   ├── __init__.py
│   └── schemas.py                 # Pydantic schemas
│
├── database/                      # Database layer
│   ├── __init__.py
│   ├── supabase_client.py        # Supabase client singleton
│   └── vector_db.py              # PostgreSQL + pgvector
│
├── scripts/                       # Utility scripts
│   ├── __init__.py
│   ├── init_db.py                # Database initialization
│   └── test_analysis.py          # Test workflow
│
└── examples/                      # Usage examples
    ├── __init__.py
    └── example_usage.py          # Python client example
```

## Component Overview

### Core Application (`main.py`)
- FastAPI application setup
- Async endpoints
- CORS configuration
- Lifecycle management
- Error handling

### Agents (`agents/`)
**8 Specialized Agents:**
1. **PlannerAgent**: Orchestrates analysis, performs web searches
2. **MarketAnalysisAgent**: Analyzes market size, trends, opportunities
3. **CompetitionAgent**: Evaluates competitive landscape
4. **RevenueAgent**: Designs revenue models
5. **CostAgent**: Analyzes cost structure
6. **GTMAgent**: Creates go-to-market strategies
7. **TargetAudienceAgent**: Identifies customer segments
8. **SuccessProbabilityAgent**: Calculates success probability
9. **CriticAgent**: Reviews and improves reports

**Orchestrator**: Coordinates agent workflow sequentially

### RAG System (`rag/`)
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Retrieval**: Vector similarity search, context building
- **Storage**: Automatic storage of reports as embeddings

### Tools (`tools/`)
- **Web Search**: DuckDuckGo integration for live market trends
- Search results embedded and injected into LLM context

### Models (`models/`)
- **Pydantic Schemas**: Request/response validation
- **Structured Output**: JSON schema enforcement

### Database (`database/`)
- **Supabase Client**: Connection management
- **Vector DB**: PostgreSQL with pgvector extension
- **Operations**: Insert, search, retrieve

### Scripts (`scripts/`)
- **init_db.py**: Initialize database schema
- **test_analysis.py**: Test complete workflow

### Examples (`examples/`)
- **example_usage.py**: Python client demonstration

## Data Flow

```
1. Request → FastAPI Endpoint
2. Orchestrator starts workflow
3. RAG retrieves similar ideas
4. Planner performs web searches
5. 8 agents analyze sequentially:
   - Market Analysis
   - Target Audience
   - Competition
   - Revenue Model
   - Cost Structure
   - Go-to-Market
   - Success Probability
   - Critic Review
6. Structured report generated
7. Report stored in vector DB
8. Response returned to client
```

## Technology Stack

- **Framework**: FastAPI
- **LLM**: Groq Llama3 via langchain-groq
- **Embeddings**: HuggingFace sentence-transformers
- **Vector DB**: Supabase PostgreSQL + pgvector
- **Web Search**: DuckDuckGo via langchain-community
- **Validation**: Pydantic
- **Async**: asyncio, httpx

## Key Features

✅ Multi-agent architecture (8 specialized agents)
✅ RAG with vector similarity search
✅ Web search for live market trends
✅ Structured JSON output
✅ Critic agent for quality review
✅ Async endpoints
✅ Error handling
✅ Health checks
✅ Docker support
✅ Production-ready

## Configuration

All configuration via environment variables in `.env`:
- GROQ_API_KEY
- SUPABASE_URL
- SUPABASE_KEY
- SUPABASE_DB_URL
- LLM_MODEL
- LLM_TEMPERATURE
- EMBEDDING_MODEL
- TOP_K_SIMILAR

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /analyze` - Analyze startup idea
- `GET /similar/{idea_id}` - Get similar ideas

## Development

- Modular architecture
- Type hints throughout
- Comprehensive error handling
- Async/await patterns
- Singleton patterns for clients
- Dependency injection

## Testing

```bash
# Initialize database
python scripts/init_db.py

# Test analysis
python scripts/test_analysis.py

# Run example
python examples/example_usage.py
```

## Deployment

See `DEPLOYMENT.md` for:
- Docker deployment
- Cloud platform deployment (Render, Railway, GCP, AWS)
- Production considerations
- Scaling strategies
