# 🚀 Quick Start Guide

## Starting the Application

### Option 1: Using the Batch Script (Recommended for Windows)

**Backend:**
```cmd
.\start_backend.bat
```

**Frontend (in a new terminal):**
```cmd
cd frontend
py -3.11 -m http.server 8080
```

### Option 2: Manual Start

**Backend:**
```powershell
$env:PYTHONIOENCODING="utf-8"
py -3.11 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (in a new terminal):**
```cmd
cd frontend
py -3.11 -m http.server 8080
```

## Access the Application

- **Frontend:** http://localhost:8080
- **Backend API Docs:** http://localhost:8000/docs
- **Backend Health:** http://localhost:8000/health

## Troubleshooting

### Issue: "Failed to analyze idea. Please try again."

**Cause:** Character encoding issue with emojis in console output on Windows.

**Solution:** Use the `start_backend.bat` script which sets proper UTF-8 encoding:
- Sets code page to 65001 (UTF-8)
- Sets PYTHONIOENCODING environment variable

### Issue: Port already in use

**Solution:**
```powershell
# Find and kill the process using port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Or use a different port
py -3.11 -m uvicorn main:app --reload --port 8001
```

### Issue: Module not found

**Solution:**
```cmd
py -3.11 -m pip install -r requirements.txt
```

## Environment Setup

Make sure your `.env` file has the required credentials:
```
GROQ_API_KEY=your_key_here
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
SUPABASE_DB_URL=your_db_url_here
```

## Testing the Application

1. Open http://localhost:8080 in your browser
2. Enter a startup idea (e.g., "AI-powered fitness app")
3. Fill in optional fields (industry, target market)
4. Click "Analyze Idea"
5. Wait for the analysis (takes 30-60 seconds)
6. View the comprehensive feasibility report

## Stopping the Servers

Press `Ctrl+C` in each terminal window to stop the servers.
