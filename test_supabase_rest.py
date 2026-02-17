"""
Test Supabase connection using REST API
"""
import os
from dotenv import load_dotenv
from database.supabase_client import SupabaseClient

load_dotenv(override=True)

def test_supabase_connection():
    print("Testing Supabase connection...")
    print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
    print(f"SUPABASE_KEY: {os.getenv('SUPABASE_KEY')[:20]}...")
    
    try:
        # Initialize client
        client = SupabaseClient()
        print("✅ Supabase client initialized")
        
        # Try to query the table
        result = client.client.table('startup_reports').select("id").limit(1).execute()
        print(f"✅ Successfully queried startup_reports table")
        print(f"   Result: {result.data}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    if success:
        print("\n🎉 Supabase connection test PASSED!")
    else:
        print("\n❌ Supabase connection test FAILED!")
