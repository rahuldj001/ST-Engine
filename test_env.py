import os
from dotenv import load_dotenv

load_dotenv(override=True)

print(f"SUPABASE_DB_URL: {os.getenv('SUPABASE_DB_URL')}")
