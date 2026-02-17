# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your credentials
```

Required credentials:
- **GROQ_API_KEY**: Get from https://console.groq.com/
- **SUPABASE_URL**: Get from your Supabase project settings
- **SUPABASE_KEY**: Get from your Supabase project settings (anon/public key)
- **SUPABASE_DB_URL**: PostgreSQL connection string from Supabase

### 3. Initialize Database
```bash
python scripts/init_db.py
```

### 4. Run the Application
```bash
python main.py
```

Visit http://localhost:8000/docs for interactive API documentation.

## Quick Test

```bash
# Test the analysis
python scripts/test_analysis.py
```

Or use curl:
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "AI-powered personal finance assistant for millennials",
    "industry": "fintech",
    "target_market": "United States"
  }'
```

## Supabase Setup

1. Create a new project at https://supabase.com
2. Go to SQL Editor
3. Run this SQL:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```
4. Get your credentials from Project Settings > API
5. Get your database URL from Project Settings > Database

## Common Issues

### Issue: "Module not found"
**Solution**: Make sure virtual environment is activated and dependencies are installed

### Issue: "Database connection failed"
**Solution**: Check your SUPABASE_DB_URL is correct and database is accessible

### Issue: "GROQ_API_KEY not set"
**Solution**: Make sure .env file exists and contains valid GROQ_API_KEY

## Next Steps

- Read the full README.md for detailed documentation
- Explore the API at http://localhost:8000/docs
- Customize agents in the `agents/` directory
- Add new features or modify existing ones

## Architecture Overview

```
Request → FastAPI → Orchestrator → [8 Agents] → Response
                         ↓
                    RAG System
                         ↓
                  Vector Database
```

The system:
1. Retrieves similar ideas from vector DB
2. Performs web searches for market trends
3. Runs 8 specialized agents in sequence
4. Generates structured JSON report
5. Reviews with critic agent
6. Stores report in vector DB

Enjoy building with the AI Startup Feasibility Engine! 🚀
