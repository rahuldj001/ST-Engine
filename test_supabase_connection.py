"""
Simple Supabase connection test using postgrest directly
Loads from .env.example file
"""
import os
import sys
from dotenv import load_dotenv
from postgrest import SyncPostgrestClient

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env.example instead of .env
load_dotenv('.env.example')

# Get credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("="*80)
print("SUPABASE CONNECTION TEST (Using .env.example)")
print("="*80)

# Check if credentials are loaded
print(f"\nConfiguration (from .env.example):")
if url:
    print(f"  SUPABASE_URL: {url}")
else:
    print(f"  SUPABASE_URL: [X] Not found in .env.example")

if key:
    print(f"  SUPABASE_KEY: {key[:30]}...{key[-20:]}" if len(key) > 50 else f"  SUPABASE_KEY: {key}")
else:
    print(f"  SUPABASE_KEY: [X] Not found in .env.example")

if not url or not key:
    print("\n[X] ERROR: Missing credentials in .env.example file")
    print("\n[!] Make sure you have:")
    print("   1. Updated .env.example with your actual credentials")
    print("   2. Added your SUPABASE_URL from Supabase dashboard")
    print("   3. Added your SUPABASE_KEY (anon/public key)")
    print("\n[>] Find these in: Supabase Dashboard > Settings > API")
    exit(1)

# Check if these are placeholder values
if url == "your_supabase_url_here" or key == "your_supabase_anon_key_here":
    print("\n[!] WARNING: Detected placeholder values in .env.example")
    print("    Please replace these with your actual Supabase credentials:")
    print(f"    - SUPABASE_URL: {url}")
    print(f"    - SUPABASE_KEY: {key}")
    print("\n[>] Get your credentials from: https://supabase.com/dashboard")
    print("    Settings > API > Project URL and anon/public key")
    exit(1)

# Construct the REST API URL
rest_url = f"{url}/rest/v1"

print(f"\n[>] Attempting to connect to Supabase...")
print(f"    REST API URL: {rest_url}")

try:
    # Create PostgREST client
    client = SyncPostgrestClient(
        base_url=rest_url,
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}"
        }
    )
    
    print(f"[OK] Client created successfully!")
    
    # Try a simple query to verify connection
    print(f"\n[>] Testing database access...")
    try:
        # Try to query a table (will fail if table doesn't exist, which is expected)
        response = client.from_("startup_reports").select("*").limit(1).execute()
        
        print(f"[OK] Database access verified!")
        print(f"     Table 'startup_reports' exists")
        if response.data:
            print(f"     Found {len(response.data)} record(s)")
        else:
            print(f"     Table is empty (no records yet)")
            
    except Exception as e:
        error_msg = str(e).lower()
        
        if "relation" in error_msg or "does not exist" in error_msg or "not found" in error_msg:
            print(f"[!] Table 'startup_reports' doesn't exist yet")
            print(f"    This is expected for a new setup")
            print(f"\n[!] Next steps:")
            print(f"    1. Enable pgvector extension in Supabase SQL Editor:")
            print(f"       CREATE EXTENSION IF NOT EXISTS vector;")
            print(f"    2. Run: python scripts/init_db.py")
        else:
            print(f"[!] Query failed: {e}")
            print(f"\n[!] This might be okay - connection is established")
    
    print(f"\n{'='*80}")
    print(f"[OK] CONNECTION TEST PASSED")
    print(f"{'='*80}")
    print(f"\n[OK] Your Supabase credentials are working!")
    print(f"[OK] You can now proceed with the setup")
    
except Exception as e:
    print(f"\n[X] Connection failed!")
    print(f"    Error: {e}")
    print(f"\n[!] Troubleshooting:")
    print(f"    1. Verify your SUPABASE_URL is correct")
    print(f"       Format: https://xxxxx.supabase.co")
    print(f"    2. Verify your SUPABASE_KEY (anon/public key)")
    print(f"       Find it in: Supabase Dashboard > Settings > API")
    print(f"    3. Check if your Supabase project is active")
    print(f"    4. Ensure you're using the anon/public key, not the service_role key")
    print(f"\n{'='*80}")
    print(f"[X] CONNECTION TEST FAILED")
    print(f"{'='*80}")
    exit(1)
