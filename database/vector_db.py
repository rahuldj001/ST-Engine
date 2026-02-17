import os
from typing import Optional, List, Dict
from database.supabase_client import SupabaseClient
from dotenv import load_dotenv

load_dotenv(override=True)


class VectorDB:
    """Supabase-based vector database using REST API and RPC functions"""
    
    def __init__(self):
        self.supabase_client = SupabaseClient()
        self.client = self.supabase_client.client
    
    def connect(self):
        """Connection is handled by Supabase client - no-op for compatibility"""
        pass
    
    def close(self):
        """Connection is handled by Supabase client - no-op for compatibility"""
        pass
    
    def initialize_schema(self):
        """
        Initialize database schema with pgvector extension
        
        Note: This should be run manually in Supabase SQL Editor:
        
        -- Enable pgvector extension
        CREATE EXTENSION IF NOT EXISTS vector;
        
        -- Create startup_reports table
        CREATE TABLE IF NOT EXISTS startup_reports (
            id SERIAL PRIMARY KEY,
            idea TEXT NOT NULL,
            embedding vector(384),
            report JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create index for vector similarity search
        CREATE INDEX IF NOT EXISTS startup_reports_embedding_idx 
        ON startup_reports 
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
        
        -- Create RPC function for similarity search
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
        """
        print("Schema initialization should be done manually in Supabase SQL Editor.")
        print("See the docstring in initialize_schema() for the SQL commands.")
    
    def insert_idea(self, idea: str, embedding: List[float], report: dict) -> int:
        """Insert a new startup idea with its embedding and report"""
        try:
            result = self.client.table('startup_reports').insert({
                'idea': idea,
                'embedding': embedding,
                'report': report
            }).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]['id']
            else:
                raise Exception("Failed to insert idea - no data returned")
        except Exception as e:
            print(f"Error inserting idea: {e}")
            raise
    
    def search_similar_ideas(self, embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Search for similar ideas using RPC function"""
        try:
            # Call the RPC function for similarity search
            result = self.client.rpc(
                'search_similar_ideas',
                {
                    'query_embedding': embedding,
                    'match_count': top_k
                }
            ).execute()
            
            if result.data:
                return result.data
            else:
                return []
        except Exception as e:
            print(f"Error searching similar ideas: {e}")
            # Return empty list if search fails (e.g., no data in database yet)
            return []
    
    def get_idea_by_id(self, idea_id: int) -> Optional[Dict]:
        """Retrieve a specific idea by ID"""
        try:
            result = self.client.table('startup_reports').select(
                'id, idea, report, created_at'
            ).eq('id', idea_id).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            else:
                return None
        except Exception as e:
            print(f"Error retrieving idea by ID: {e}")
            return None


# Global instance
vector_db = VectorDB()
