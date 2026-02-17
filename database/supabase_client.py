import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)


class SupabaseClient:
    """Singleton Supabase client for database operations"""
    
    _instance: Optional['SupabaseClient'] = None
    _client: Optional[Client] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
            
            self._client = create_client(supabase_url, supabase_key)
    
    @property
    def client(self) -> Client:
        """Get the Supabase client instance"""
        if self._client is None:
            raise RuntimeError("Supabase client not initialized")
        return self._client
    
    async def health_check(self) -> bool:
        """Check if database connection is healthy"""
        try:
            # Try to query a simple table or perform a basic operation
            result = self._client.table('startup_reports').select("id").limit(1).execute()
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False


def get_supabase_client() -> Client:
    """Dependency injection for Supabase client"""
    return SupabaseClient().client
