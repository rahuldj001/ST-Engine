# Database Setup Guide

## Overview

The AI Startup Feasibility Engine uses **Supabase** as the database backend with **pgvector** extension for vector similarity search.

## Architecture

- **Supabase REST API**: All database operations go through Supabase's REST client
- **Vector Search**: Uses PostgreSQL RPC function for similarity search
- **No Direct PostgreSQL Connection**: Removed psycopg2 dependency for better compatibility

## Setup Instructions

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project or use an existing one
3. Note down your:
   - Project URL (e.g., `https://xxxxx.supabase.co`)
   - Anon/Public Key
   - Database URL (for reference only, not used in code)

### 2. Run Database Setup SQL

1. Open your Supabase project dashboard
2. Go to **SQL Editor**
3. Copy the contents of `database/setup_supabase.sql`
4. Paste and run the SQL script

This will:
- Enable the `vector` extension
- Create the `startup_reports` table
- Create an index for vector similarity search
- Create the `search_similar_ideas` RPC function

### 3. Configure Environment Variables

Update your `.env` file with your Supabase credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

**Note**: You no longer need `SUPABASE_DB_URL` since we're using the REST API.

### 4. Verify Setup

Run the test script to verify the connection:

```bash
py -3.11 test_supabase_connection.py
```

## Database Schema

### startup_reports Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| idea | TEXT | The startup idea description |
| embedding | vector(384) | Vector embedding of the idea |
| report | JSONB | Full feasibility report |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### RPC Function: search_similar_ideas

**Parameters:**
- `query_embedding`: vector(384) - The embedding to search for
- `match_count`: int - Number of results to return (default: 5)

**Returns:**
- `id`: int - Idea ID
- `idea`: text - Idea description
- `report`: jsonb - Feasibility report
- `similarity`: float - Similarity score (0-1)

**Example Usage (in Python):**
```python
from database.vector_db import vector_db

# Search for similar ideas
embedding = [0.1, 0.2, ...]  # 384-dimensional vector
results = vector_db.search_similar_ideas(embedding, top_k=5)
```

## Troubleshooting

### Issue: "Function search_similar_ideas does not exist"

**Solution**: Run the SQL setup script in Supabase SQL Editor.

### Issue: "Permission denied for function search_similar_ideas"

**Solution**: Grant execute permissions:
```sql
GRANT EXECUTE ON FUNCTION search_similar_ideas TO authenticated;
GRANT EXECUTE ON FUNCTION search_similar_ideas TO anon;
```

### Issue: "Extension vector does not exist"

**Solution**: Enable the pgvector extension:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## Migration from Direct PostgreSQL

If you're migrating from the old `psycopg2`-based implementation:

1. ✅ Remove `psycopg2-binary`, `vecs`, and `pgvector` from requirements.txt
2. ✅ Update `database/vector_db.py` to use Supabase client
3. ✅ Run the SQL setup script in Supabase
4. ✅ Update `.env` to remove `SUPABASE_DB_URL`
5. ✅ Restart the backend server

## Benefits of Supabase REST API

- ✅ No direct database connection issues
- ✅ Better security (no database credentials in code)
- ✅ Automatic connection pooling
- ✅ Works behind firewalls and proxies
- ✅ Built-in authentication and authorization
- ✅ Real-time subscriptions (future feature)
