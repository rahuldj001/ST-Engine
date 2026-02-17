# Setup Checklist

Use this checklist to ensure your AI Startup Feasibility Engine is properly configured and ready to use.

---

## ✅ Pre-Installation Checklist

- [ ] Python 3.9 or higher installed
- [ ] pip package manager available
- [ ] Virtual environment tool available (venv)
- [ ] Git installed (optional, for version control)
- [ ] Text editor or IDE ready

---

## ✅ Account Setup Checklist

### Groq Account
- [ ] Create account at https://console.groq.com/
- [ ] Generate API key
- [ ] Copy API key to safe location
- [ ] Verify API key works

### Supabase Account
- [ ] Create account at https://supabase.com/
- [ ] Create new project
- [ ] Note project URL
- [ ] Copy anon/public key from Settings > API
- [ ] Copy database connection string from Settings > Database
- [ ] Enable pgvector extension in SQL Editor:
  ```sql
  CREATE EXTENSION IF NOT EXISTS vector;
  ```

---

## ✅ Installation Checklist

- [ ] Navigate to project directory
- [ ] Create virtual environment:
  ```bash
  python -m venv venv
  ```
- [ ] Activate virtual environment:
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
- [ ] Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Verify installation (no errors)

---

## ✅ Configuration Checklist

- [ ] Copy `.env.example` to `.env`:
  ```bash
  cp .env.example .env
  ```
- [ ] Edit `.env` file with your credentials:
  - [ ] `GROQ_API_KEY` = your Groq API key
  - [ ] `SUPABASE_URL` = your Supabase project URL
  - [ ] `SUPABASE_KEY` = your Supabase anon key
  - [ ] `SUPABASE_DB_URL` = your PostgreSQL connection string
- [ ] Verify all required variables are set
- [ ] Optional: Configure other settings (LLM model, temperature, etc.)

---

## ✅ Database Setup Checklist

- [ ] Ensure Supabase project is running
- [ ] Verify pgvector extension is enabled
- [ ] Run database initialization script:
  ```bash
  python scripts/init_db.py
  ```
- [ ] Verify tables created successfully:
  - [ ] `startup_ideas` table exists
  - [ ] Vector index created
- [ ] Check for any error messages

---

## ✅ Application Startup Checklist

- [ ] Virtual environment is activated
- [ ] All environment variables are set
- [ ] Database is initialized
- [ ] Run the application:
  ```bash
  python main.py
  ```
- [ ] Application starts without errors
- [ ] Note the URL (default: http://localhost:8000)

---

## ✅ Verification Checklist

### Health Check
- [ ] Open browser to http://localhost:8000/health
- [ ] Response shows `"status": "healthy"`
- [ ] Response shows `"database_connected": true`

### Interactive Documentation
- [ ] Open browser to http://localhost:8000/docs
- [ ] Swagger UI loads successfully
- [ ] All endpoints visible:
  - [ ] GET /
  - [ ] GET /health
  - [ ] POST /analyze
  - [ ] GET /similar/{idea_id}

### Test Analysis
- [ ] Run test script:
  ```bash
  python scripts/test_analysis.py
  ```
- [ ] Script completes without errors
- [ ] Report is generated
- [ ] All sections populated:
  - [ ] Market analysis
  - [ ] Target audience
  - [ ] Revenue model
  - [ ] Competition analysis
  - [ ] Cost structure
  - [ ] Go-to-market
  - [ ] Success probability
  - [ ] Best location
  - [ ] Critique

---

## ✅ API Testing Checklist

### Using Swagger UI
- [ ] Navigate to http://localhost:8000/docs
- [ ] Click on POST /analyze
- [ ] Click "Try it out"
- [ ] Enter test data:
  ```json
  {
    "idea": "AI-powered fitness app",
    "industry": "fitness tech",
    "target_market": "United States"
  }
  ```
- [ ] Click "Execute"
- [ ] Wait for response (60-120 seconds)
- [ ] Verify 200 OK response
- [ ] Verify report structure is correct

### Using cURL
- [ ] Run cURL command:
  ```bash
  curl -X POST "http://localhost:8000/analyze" \
    -H "Content-Type: application/json" \
    -d '{"idea": "AI fitness app", "industry": "fitness tech", "target_market": "United States"}'
  ```
- [ ] Verify response received
- [ ] Verify JSON structure

### Using Python Script
- [ ] Run example script:
  ```bash
  python examples/example_usage.py
  ```
- [ ] Script completes successfully
- [ ] Report saved to file
- [ ] Review generated report

---

## ✅ Troubleshooting Checklist

If something doesn't work, check:

### Environment Issues
- [ ] Virtual environment is activated
- [ ] All dependencies installed (`pip list`)
- [ ] Python version is 3.9+ (`python --version`)

### Configuration Issues
- [ ] `.env` file exists
- [ ] All required variables are set
- [ ] No typos in variable names
- [ ] API keys are valid
- [ ] Database URL is correct

### Database Issues
- [ ] Supabase project is running
- [ ] pgvector extension is enabled
- [ ] Connection string is correct
- [ ] Firewall allows connection
- [ ] Database initialization ran successfully

### API Issues
- [ ] Application is running
- [ ] Port 8000 is not in use by another app
- [ ] No firewall blocking localhost
- [ ] Request format is correct
- [ ] Timeout is set appropriately (120+ seconds)

### LLM Issues
- [ ] Groq API key is valid
- [ ] Groq service is available
- [ ] Rate limits not exceeded
- [ ] Model name is correct

---

## ✅ Production Deployment Checklist

### Security
- [ ] Never commit `.env` file
- [ ] Use environment-specific API keys
- [ ] Configure CORS for production domains
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Use HTTPS
- [ ] Set up secrets management

### Performance
- [ ] Enable response compression
- [ ] Implement caching layer
- [ ] Use connection pooling
- [ ] Optimize vector search indexes
- [ ] Set up CDN for static assets

### Monitoring
- [ ] Set up application monitoring (Sentry, DataDog)
- [ ] Configure logging aggregation
- [ ] Set up error alerts
- [ ] Monitor API response times
- [ ] Track database performance

### Deployment
- [ ] Choose deployment platform
- [ ] Configure environment variables
- [ ] Set up CI/CD pipeline
- [ ] Configure health checks
- [ ] Set up load balancing (if needed)
- [ ] Configure auto-scaling (if needed)
- [ ] Test in staging environment
- [ ] Deploy to production
- [ ] Verify production deployment

---

## ✅ Documentation Review Checklist

- [ ] Read README.md
- [ ] Review QUICKSTART.md
- [ ] Study API.md
- [ ] Understand ARCHITECTURE.md
- [ ] Review STRUCTURE.md
- [ ] Read DEPLOYMENT.md
- [ ] Check PROJECT_SUMMARY.md

---

## ✅ Next Steps Checklist

### Immediate
- [ ] Test with your own startup ideas
- [ ] Review generated reports
- [ ] Understand agent workflow
- [ ] Explore API endpoints

### Short Term
- [ ] Customize agent prompts
- [ ] Adjust LLM parameters
- [ ] Add custom validation
- [ ] Implement caching

### Long Term
- [ ] Deploy to production
- [ ] Build web UI
- [ ] Add authentication
- [ ] Implement webhooks
- [ ] Add PDF export
- [ ] Scale infrastructure

---

## 📝 Notes

Use this space to track your setup progress and any issues encountered:

```
Date: _______________

Issues Encountered:
- 
- 
- 

Solutions Applied:
- 
- 
- 

Custom Configurations:
- 
- 
- 

Next Actions:
- 
- 
- 
```

---

## ✅ Setup Complete!

When all items are checked, you're ready to:
- 🚀 Analyze startup ideas
- 📊 Generate feasibility reports
- 🔍 Explore similar ideas
- 🎯 Deploy to production

**Happy analyzing!** 🎉
