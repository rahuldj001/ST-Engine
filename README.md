# 🚀 AI Startup Feasibility Engine

> **Production-ready FastAPI application for AI-powered startup feasibility analysis**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-121212?style=for-the-badge)](https://www.langchain.com/)

---

## 📋 Overview

An intelligent multi-agent system that analyzes startup ideas and generates comprehensive feasibility reports using:
- **8 Specialized AI Agents** for different analysis aspects
- **RAG (Retrieval-Augmented Generation)** with vector similarity search
- **Live Web Search** for market trends
- **Groq Llama3** for powerful LLM capabilities
- **Structured JSON Output** for easy integration

---

## ✨ Key Features

### 🤖 Multi-Agent Architecture
- **Planner**: Strategic planning + web search
- **Market Analyst**: Market size, trends, opportunities
- **Competition Analyst**: Competitive landscape
- **Revenue Strategist**: Revenue model design
- **Cost Analyst**: Cost structure analysis
- **GTM Strategist**: Go-to-market strategy
- **Audience Analyst**: Customer segmentation
- **Success Analyst**: Probability scoring + location
- **Critic**: Quality review & improvements

### 🔍 RAG Implementation
- HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- Supabase PostgreSQL with pgvector extension
- Automatic storage and retrieval of similar ideas
- Context-aware analysis based on historical data

### 🌐 Web Search Integration
- DuckDuckGo search for live market intelligence
- Embedded search results in LLM context
- Real-time trend analysis

<img width="400" height="1536" alt="400" src="https://github.com/user-attachments/assets/3b1f4432-a73a-4bdc-9768-f5dbd9f59f06" />







### 📊 Structured Output
```json
{
  "market_analysis": "...",
  "target_audience": "...",
  "revenue_model": "...",
  "competition_analysis": "...",
  "cost_structure": "...",
  "go_to_market": "...",
  "success_probability": 72.5,
  "best_location": "San Francisco, CA"
}
```

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2️⃣ Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

**Required:**
- `GROQ_API_KEY` - Get from [Groq Console](https://console.groq.com/)
- `SUPABASE_URL` - Get from [Supabase](https://supabase.com/)
- `SUPABASE_KEY` - Supabase anon/public key
- `SUPABASE_DB_URL` - PostgreSQL connection string

### 3️⃣ Initialize Database
```bash
python scripts/init_db.py
```

### 4️⃣ Run Application
```bash
python main.py
```

Visit **http://localhost:8000/docs** for interactive API documentation! 🎉

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📘 README.md](README.md) | Complete documentation |
| [⚡ QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [📡 API.md](API.md) | API reference |
| [🚢 DEPLOYMENT.md](DEPLOYMENT.md) | Deployment guide |
| [🏗️ ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [📁 STRUCTURE.md](STRUCTURE.md) | Project structure |
| [📝 PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Complete summary |

---

## 🎯 Example Usage

### cURL
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "AI-powered meal planning app for busy professionals",
    "industry": "food tech",
    "target_market": "United States"
  }'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "idea": "AI-powered meal planning app",
        "industry": "food tech",
        "target_market": "United States"
    }
)

report = response.json()
print(f"Success Probability: {report['report']['success_probability']}%")
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    idea: 'AI-powered meal planning app',
    industry: 'food tech',
    target_market: 'United States'
  })
});

const report = await response.json();
console.log(`Success: ${report.report.success_probability}%`);
```

---

## 🏗️ Project Structure

```
ST Engine/
├── main.py                 # FastAPI application
├── agents/                 # 8 AI agents + orchestrator
├── rag/                    # RAG system (embeddings + retrieval)
├── tools/                  # Web search integration
├── models/                 # Pydantic schemas
├── database/               # Supabase + pgvector
├── scripts/                # Utility scripts
├── examples/               # Usage examples
└── docs/                   # Documentation
```

**Total Files:** 34+ | **Lines of Code:** 2,500+

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI + Uvicorn |
| **LLM** | Groq Llama3-70B |
| **Embeddings** | HuggingFace sentence-transformers |
| **Vector DB** | Supabase PostgreSQL + pgvector |
| **Web Search** | DuckDuckGo (LangChain) |
| **Validation** | Pydantic |
| **Container** | Docker + Docker Compose |

---

## 🐳 Docker Deployment

```bash
# Build and run
docker build -t ai-feasibility-engine .
docker run -d -p 8000:8000 --env-file .env ai-feasibility-engine

# Or use Docker Compose
docker-compose up -d
```

---

## ☁️ Cloud Deployment

Deploy to any platform:
- ✅ **Render** - One-click deployment
- ✅ **Railway** - Auto-deploy from Git
- ✅ **Google Cloud Run** - Serverless containers
- ✅ **AWS ECS** - Elastic Container Service
- ✅ **Any Docker platform**

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 🧪 Testing

```bash
# Test complete workflow
python scripts/test_analysis.py

# Example API usage
python examples/example_usage.py

# Initialize database
python scripts/init_db.py
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint |
| `GET` | `/health` | Health check |
| `POST` | `/analyze` | Analyze startup idea |
| `GET` | `/similar/{id}` | Get similar ideas |

**Interactive Docs:** http://localhost:8000/docs

---

## 🎨 Code Quality

- ✅ Modular architecture
- ✅ Type hints throughout
- ✅ Async/await patterns
- ✅ Comprehensive error handling
- ✅ Clean separation of concerns
- ✅ Production-ready code

---

## 🔒 Security

- Environment variable configuration
- Input validation with Pydantic
- CORS middleware
- Docker non-root user
- No sensitive data in code

**Production Recommendations:**
- Add API authentication
- Implement rate limiting
- Use HTTPS
- Set up monitoring

---

## 📈 Performance

- Async endpoints for concurrency
- Efficient vector similarity search
- Connection pooling
- Cached embedding models
- Optimized database indexes

**Processing Time:** 60-120 seconds per analysis

---

## 🛠️ Customization

### Add New Agent
1. Create class in `agents/`
2. Inherit from `BaseAgent`
3. Implement `execute()` method
4. Add to orchestrator

### Modify Output
1. Edit `models/schemas.py`
2. Update agent prompts
3. Adjust orchestrator

### Change LLM
1. Update `agents/base_agent.py`
2. Install provider package
3. Update environment variables

---

## 📝 Example Output

```json
{
  "idea": "AI fitness class booking app",
  "report": {
    "market_analysis": "The fitness tech market is valued at $30B...",
    "target_audience": "Primary: Urban professionals aged 25-40...",
    "revenue_model": "Freemium with premium subscriptions at $9.99/mo...",
    "competition_analysis": "Main competitors: ClassPass, Mindbody...",
    "cost_structure": "Initial: $75K, Monthly burn: $15K...",
    "go_to_market": "Launch in SF, NYC, LA with influencer partnerships...",
    "success_probability": 72.5,
    "best_location": "San Francisco, CA"
  },
  "similar_ideas": ["Fitness marketplace app...", "..."],
  "sources_used": ["fitness tech market trends 2026"],
  "critique": "Strong market opportunity but competition is fierce..."
}
```

---

## 🎯 Use Cases

- 🚀 **Startup Founders** - Validate ideas before building
- 💼 **Investors** - Quick feasibility assessment
- 🏢 **Accelerators** - Screen applications
- 📊 **Consultants** - Generate market reports
- 🎓 **Students** - Learn startup analysis
- 🔬 **Researchers** - Study startup patterns

---

## 🤝 Contributing

Contributions welcome! Please ensure:
- Code follows existing patterns
- Type hints are included
- Error handling is comprehensive
- Documentation is updated

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/)
- [Groq](https://groq.com/)
- [Supabase](https://supabase.com/)
- [HuggingFace](https://huggingface.co/)

---

## 📧 Support

- 📚 Check the [documentation](README.md)
- 🔍 Review [API docs](API.md)
- 🐛 Report issues
- 💬 Ask questions

---

## ⭐ Star This Project

If you find this useful, please star the repository!

---

<div align="center">

**Built with ❤️ using FastAPI, LangChain, Groq, and Supabase**

[Get Started](QUICKSTART.md) • [Documentation](README.md) • [API Reference](API.md)

</div>
