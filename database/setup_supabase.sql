-- AI Startup Feasibility Engine - Supabase Database Setup
-- Run this SQL in your Supabase SQL Editor

-- Step 1: Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Create startup_reports table
CREATE TABLE IF NOT EXISTS startup_reports (
    id SERIAL PRIMARY KEY,
    idea TEXT NOT NULL,
    embedding vector(384),
    report JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Create index for vector similarity search
CREATE INDEX IF NOT EXISTS startup_reports_embedding_idx 
ON startup_reports 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Step 4: Create RPC function for similarity search
CREATE OR REPLACE FUNCTION search_similar_ideas(
    query_embedding vector(384),
    match_count int DEFAULT 5
)
RETURNS TABLE (
    id int,
    idea text,
    report jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        startup_reports.id,
        startup_reports.idea,
        startup_reports.report,
        1 - (startup_reports.embedding <=> query_embedding) as similarity
    FROM startup_reports
    WHERE startup_reports.embedding IS NOT NULL
    ORDER BY startup_reports.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Step 5: Grant permissions (optional, adjust as needed)
-- GRANT ALL ON startup_reports TO authenticated;
-- GRANT EXECUTE ON FUNCTION search_similar_ideas TO authenticated;

-- Verification queries:
-- SELECT * FROM startup_reports LIMIT 5;
-- SELECT search_similar_ideas(ARRAY[0.1, 0.2, ...]::vector(384), 5);
