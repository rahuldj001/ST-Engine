# 🚀 How to Start the Backend

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
python -m pip install fastapi uvicorn[standard] langchain langchain-groq python-dotenv psycopg2-binary
```

### Step 2: Set Up Environment Variables
Make sure your `.env` file exists with your credentials:
```bash
# Copy from .env.example if needed
copy .env.example .env
```

Required variables:
- `GROQ_API_KEY` - Your Groq API key
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key
- `SUPABASE_DB_URL` - Your Supabase database connection string

### Step 3: Start the Server
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: **http://localhost:8000**

---

## ⚠️ Troubleshooting

### Issue: PyTorch DLL Error (Visual C++ Required)

If you see an error about `c10.dll` or Visual C++ Redistributable:

**Solution 1: Install Visual C++ Redistributable**
1. Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Install it
3. Restart your terminal
4. Run the server again

**Solution 2: Use CPU-only PyTorch (Lighter)**
```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Solution 3: Skip ML Dependencies (Testing Only)**
For quick testing without ML features:
```bash
# Comment out these imports in main.py temporarily:
# from rag.embeddings import embedding_service
# from rag.retrieval import rag_service
```

---

## 📊 Verify Backend is Running

### Check Health Endpoint
Open in browser: http://localhost:8000/health

Or use curl:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.2.0",
  "database_connected": true
}
```

### View API Documentation
Open in browser: http://localhost:8000/docs

This shows the interactive Swagger UI with all API endpoints.

---

## 🔌 API Endpoints

Once running, the backend provides:

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `POST /api/analyze` - Analyze startup idea (main endpoint)
- `GET /similar/{idea_id}` - Get similar ideas

---

## 🎯 Test the Full Stack

### 1. Start Backend (Terminal 1)
```bash
cd "c:/Users/ictadmin/Desktop/ST Engine"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Frontend (Terminal 2)
```bash
cd "c:/Users/ictadmin/Desktop/ST Engine/frontend"
python -m http.server 8080
```

### 3. Open in Browser
- Frontend: http://localhost:8080
- Backend API Docs: http://localhost:8000/docs
- Backend Health: http://localhost:8000/health

---

## 🐛 Common Issues

### Port Already in Use
```bash
# Error: Address already in use
# Solution: Use a different port
python -m uvicorn main:app --reload --port 8001
```

### Module Not Found
```bash
# Error: ModuleNotFoundError: No module named 'X'
# Solution: Install the missing module
python -m pip install X
```

### Database Connection Failed
```bash
# Check your .env file has correct credentials
# Test connection with:
python test_supabase_connection.py
```

---

## 📝 Development Mode

The `--reload` flag enables auto-reload on code changes:
```bash
python -m uvicorn main:app --reload
```

For production, remove `--reload`:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔐 Security Notes

- The backend allows CORS from all origins (`allow_origins=["*"]`)
- For production, update `main.py` to restrict origins:
  ```python
  allow_origins=["https://yourdomain.com"]
  ```

---

## 📦 Full Installation (All Features)

For complete functionality including ML features:

```bash
# Install all dependencies
python -m pip install -r requirements.txt

# This includes:
# - FastAPI & Uvicorn (API server)
# - LangChain & Groq (LLM integration)
# - Sentence Transformers (Embeddings)
# - Supabase & pgvector (Database)
# - DuckDuckGo Search (Web search)
```

---

## ✅ Success Indicators

When the backend starts successfully, you should see:
```
🚀 Starting AI Startup Feasibility Engine...
📦 Initializing database schema...
✅ Database schema initialized
🔌 Connecting to Supabase...
✅ Supabase connected
✅ Application started successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using WatchFiles
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🎉 You're Ready!

Once you see the success messages, your backend is running and ready to accept requests from the frontend!

Test it by submitting a startup idea through the frontend at http://localhost:8080
