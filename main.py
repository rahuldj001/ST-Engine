import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

from models.schemas import StartupIdeaRequest, FeasibilityResponse, HealthResponse
from agents.orchestrator import orchestrator
from database.vector_db import vector_db
from database.supabase_client import SupabaseClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events"""
    # Startup
    print("Starting AI Startup Feasibility Engine...")
    
    # Initialize database schema
    try:
        print("Initializing database schema...")
        vector_db.initialize_schema()
        print("Database schema initialized")
    except Exception as e:
        print(f"Database initialization warning: {e}")
    
    # Initialize Supabase client
    try:
        print("Connecting to Supabase...")
        supabase_client = SupabaseClient()
        print("Supabase connected")
    except Exception as e:
        print(f"Supabase connection warning: {e}")
    
    print("Application started successfully!")
    
    yield
    
    # Shutdown
    print("Shutting down application...")
    vector_db.close()
    print("Application shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "AI Startup Feasibility Engine"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="Production-ready FastAPI application for AI-powered startup feasibility analysis with multi-agent architecture and RAG",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "AI Startup Feasibility Engine API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    # Check database connection
    db_connected = False
    try:
        supabase_client = SupabaseClient()
        db_connected = await supabase_client.health_check()
    except Exception as e:
        print(f"Health check error: {e}")
    
    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        version=os.getenv("APP_VERSION", "1.0.0"),
        database_connected=db_connected
    )


@app.post(
    "/api/analyze",
    response_model=FeasibilityResponse,
    status_code=status.HTTP_200_OK,
    tags=["Analysis"]
)
async def analyze_startup_idea(request: StartupIdeaRequest):
    """
    Analyze a startup idea and generate a comprehensive feasibility report
    
    This endpoint:
    1. Retrieves similar ideas from the vector database (RAG)
    2. Performs web searches for market trends
    3. Orchestrates 8 specialized AI agents to analyze different aspects
    4. Generates a structured feasibility report
    5. Reviews the report with a critic agent
    6. Stores the report in the vector database for future reference
    
    Args:
        request: Startup idea request with idea description and optional metadata
        
    Returns:
        Comprehensive feasibility report with structured analysis
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Orchestrate the multi-agent analysis
        response = await orchestrator.analyze_startup_idea(
            idea=request.idea,
            industry=request.industry or "general",
            target_market=request.target_market or "global"
        )
        
        return response
        
    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/similar/{idea_id}", tags=["Analysis"])
async def get_similar_ideas(idea_id: int, top_k: int = 5):
    """
    Retrieve a stored idea and find similar ideas
    
    Args:
        idea_id: ID of the stored idea
        top_k: Number of similar ideas to retrieve
        
    Returns:
        The idea and similar ideas
        
    Raises:
        HTTPException: If idea not found
    """
    try:
        # Get the idea
        idea_data = vector_db.get_idea_by_id(idea_id)
        
        if not idea_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Idea with ID {idea_id} not found"
            )
        
        # Get similar ideas
        from rag.retrieval import rag_service
        similar_ideas = await rag_service.retrieve_similar_ideas(idea_data["idea"])
        
        return {
            "idea": idea_data,
            "similar_ideas": similar_ideas[:top_k]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving similar ideas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve similar ideas: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
