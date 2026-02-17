"""
Database initialization script for Supabase PostgreSQL with pgvector
Run this script to set up the database schema
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.vector_db import vector_db

load_dotenv()


def main():
    """Initialize the database schema"""
    print("🚀 Initializing database schema...")
    
    try:
        vector_db.initialize_schema()
        print("✅ Database schema initialized successfully!")
        print("\nCreated tables:")
        print("  - startup_reports (with vector embeddings)")
        print("\nCreated indexes:")
        print("  - startup_reports_embedding_idx (IVFFlat for cosine similarity)")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)
    
    finally:
        vector_db.close()


if __name__ == "__main__":
    main()
