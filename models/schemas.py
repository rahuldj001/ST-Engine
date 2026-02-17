from pydantic import BaseModel, Field
from typing import Optional


class StartupIdeaRequest(BaseModel):
    """Request model for startup feasibility analysis"""
    idea: str = Field(..., description="The startup idea to analyze", min_length=10)
    industry: Optional[str] = Field(None, description="Industry sector")
    target_market: Optional[str] = Field(None, description="Target market or geography")


class FeasibilityReport(BaseModel):
    """Structured output schema for feasibility analysis"""
    market_analysis: str = Field(..., description="Comprehensive market analysis")
    target_audience: str = Field(..., description="Identified target audience and demographics")
    revenue_model: str = Field(..., description="Proposed revenue model and monetization strategy")
    competition_analysis: str = Field(..., description="Analysis of competitors and market positioning")
    cost_structure: str = Field(..., description="Expected cost structure and burn rate")
    go_to_market: str = Field(..., description="Go-to-market strategy and channels")
    success_probability: float = Field(..., description="Success probability score (0-100)", ge=0, le=100)
    best_location: str = Field(..., description="Recommended location for the startup")

from typing import Dict, Any

class EvaluationMetrics(BaseModel):
    total_tokens: Optional[int] = None
    execution_time: Optional[float] = None
    overall_confidence: Optional[float] = None
    hallucination_risk: Optional[str] = None
    retrieval_metrics: Optional[Dict[str, Any]] = None
    web_search_metrics: Optional[Dict[str, Any]] = None
    agent_metrics: Optional[Dict[str, Any]] = None

class FeasibilityResponse(BaseModel):
    idea: str
    report: FeasibilityReport
    similar_ideas: list[str] = Field(default_factory=list)
    sources_used: list[str] = Field(default_factory=list)
    critique: Optional[str] = None
    evaluation_metrics: Optional[Dict[str, Any]] = None
    hallucination_report: Optional[Dict[str, Any]] = None




class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    database_connected: bool 
