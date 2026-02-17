"""
Token usage tracking and evaluation metrics
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class AgentMetrics:
    """Metrics for a single agent execution"""
    agent_name: str
    tokens_used: int = 0
    execution_time_ms: float = 0.0
    confidence_score: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class RetrievalMetrics:
    """Metrics for RAG retrieval"""
    similar_ideas_count: int = 0
    top_similarity_score: float = 0.0
    avg_similarity_score: float = 0.0
    similarity_scores: List[float] = field(default_factory=list)
    retrieval_time_ms: float = 0.0


@dataclass
class SearchMetrics:
    """Metrics for web search"""
    search_performed: bool = False
    queries_count: int = 0
    results_found: int = 0
    search_time_ms: float = 0.0


class EvaluationMetrics:
    """
    Comprehensive evaluation metrics tracker for the entire analysis workflow
    """
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all metrics"""
        self.total_tokens: int = 0
        self.agent_metrics: List[AgentMetrics] = []
        self.retrieval_metrics: Optional[RetrievalMetrics] = None
        self.search_metrics: Optional[SearchMetrics] = None
        self.overall_confidence: float = 0.0
        self.hallucination_risk: str = "LOW"
        self.hallucination_flags: List[str] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_execution_time_ms: float = 0.0
    
    def start_tracking(self):
        """Start tracking execution time"""
        self.start_time = datetime.now()
    
    def end_tracking(self):
        """End tracking and calculate total time"""
        self.end_time = datetime.now()
        if self.start_time:
            delta = self.end_time - self.start_time
            self.total_execution_time_ms = delta.total_seconds() * 1000
    
    def add_agent_metrics(self, agent_name: str, tokens: int, execution_time_ms: float, confidence: float = 0.0):
        """
        Add metrics for an agent execution
        
        Args:
            agent_name: Name of the agent
            tokens: Estimated tokens used
            execution_time_ms: Execution time in milliseconds
            confidence: Confidence score (0-1)
        """
        metrics = AgentMetrics(
            agent_name=agent_name,
            tokens_used=tokens,
            execution_time_ms=execution_time_ms,
            confidence_score=confidence
        )
        self.agent_metrics.append(metrics)
        self.total_tokens += tokens
    
    def set_retrieval_metrics(self, similar_ideas: List[Dict], retrieval_time_ms: float):
        """
        Set RAG retrieval metrics
        
        Args:
            similar_ideas: List of similar ideas with similarity scores
            retrieval_time_ms: Retrieval time in milliseconds
        """
        similarity_scores = [
            item.get('similarity', 0.0) 
            for item in similar_ideas
        ]
        
        self.retrieval_metrics = RetrievalMetrics(
            similar_ideas_count=len(similar_ideas),
            top_similarity_score=max(similarity_scores) if similarity_scores else 0.0,
            avg_similarity_score=sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0,
            similarity_scores=similarity_scores,
            retrieval_time_ms=retrieval_time_ms
        )
    
    def set_search_metrics(self, search_performed: bool, queries: List[str], results: List[Dict], search_time_ms: float):
        """
        Set web search metrics
        
        Args:
            search_performed: Whether search was performed
            queries: List of search queries
            results: List of search results
            search_time_ms: Search time in milliseconds
        """
        results_count = sum(1 for r in results if r.get('results'))
        
        self.search_metrics = SearchMetrics(
            search_performed=search_performed,
            queries_count=len(queries),
            results_found=results_count,
            search_time_ms=search_time_ms
        )
    
    def calculate_overall_confidence(self) -> float:
        """
        Calculate overall confidence score based on agent confidences
        
        Returns:
            Overall confidence score (0-1)
        """
        if not self.agent_metrics:
            return 0.0
        
        # Weight different agents differently
        weights = {
            "Planner": 0.1,
            "Market Analyst": 0.15,
            "Competition Analyst": 0.15,
            "Revenue Strategist": 0.15,
            "Cost Analyst": 0.1,
            "GTM Strategist": 0.1,
            "Audience Analyst": 0.1,
            "Success Probability Analyst": 0.1,
            "Critic": 0.05
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metrics in self.agent_metrics:
            weight = weights.get(metrics.agent_name, 0.1)
            weighted_sum += metrics.confidence_score * weight
            total_weight += weight
        
        self.overall_confidence = weighted_sum / total_weight if total_weight > 0 else 0.0
        return self.overall_confidence
    
    def assess_hallucination_risk(self) -> str:
        """
        Assess hallucination risk based on available data
        
        Returns:
            Risk level: LOW, MEDIUM, HIGH, CRITICAL
        """
        flags = []
        risk_score = 0
        
        # Check if web search was performed and found results
        if self.search_metrics:
            if not self.search_metrics.search_performed:
                flags.append("No web search performed")
                risk_score += 2
            elif self.search_metrics.results_found == 0:
                flags.append("Web search returned no results")
                risk_score += 3
        
        # Check retrieval similarity scores
        if self.retrieval_metrics:
            if self.retrieval_metrics.similar_ideas_count == 0:
                flags.append("No similar ideas found in database")
                risk_score += 2
            elif self.retrieval_metrics.top_similarity_score < 0.3:
                flags.append(f"Low similarity to existing ideas (max: {self.retrieval_metrics.top_similarity_score:.2f})")
                risk_score += 1
        
        # Check overall confidence
        if self.overall_confidence < 0.5:
            flags.append(f"Low overall confidence ({self.overall_confidence:.2f})")
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 5:
            risk_level = "CRITICAL"
        elif risk_score >= 3:
            risk_level = "HIGH"
        elif risk_score >= 1:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        self.hallucination_risk = risk_level
        self.hallucination_flags = flags
        
        return risk_level
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics summary
        
        Returns:
            Dictionary with all metrics
        """
        return {
            "total_tokens": self.total_tokens,
            "total_execution_time_ms": self.total_execution_time_ms,
            "overall_confidence": round(self.overall_confidence, 3),
            "hallucination_risk": self.hallucination_risk,
            "hallucination_flags": self.hallucination_flags,
            "agent_metrics": [
                {
                    "agent": m.agent_name,
                    "tokens": m.tokens_used,
                    "execution_time_ms": round(m.execution_time_ms, 2),
                    "confidence": round(m.confidence_score, 3)
                }
                for m in self.agent_metrics
            ],
            "retrieval_metrics": {
                "similar_ideas_count": self.retrieval_metrics.similar_ideas_count,
                "top_similarity": round(self.retrieval_metrics.top_similarity_score, 3),
                "avg_similarity": round(self.retrieval_metrics.avg_similarity_score, 3),
                "retrieval_time_ms": round(self.retrieval_metrics.retrieval_time_ms, 2)
            } if self.retrieval_metrics else None,
            "search_metrics": {
                "search_performed": self.search_metrics.search_performed,
                "queries_count": self.search_metrics.queries_count,
                "results_found": self.search_metrics.results_found,
                "search_time_ms": round(self.search_metrics.search_time_ms, 2)
            } if self.search_metrics else None
        }
    
    def print_summary(self):
        """Print formatted metrics summary"""
        print("\n" + "="*80)
        print("EVALUATION METRICS SUMMARY")
        print("="*80)
        
        print(f"\n📊 OVERALL METRICS:")
        print(f"  Total Tokens Used: {self.total_tokens:,}")
        print(f"  Total Execution Time: {self.total_execution_time_ms/1000:.2f}s")
        print(f"  Overall Confidence: {self.overall_confidence:.1%}")
        print(f"  Hallucination Risk: {self.hallucination_risk}")
        
        if self.hallucination_flags:
            print(f"\n⚠️  HALLUCINATION FLAGS:")
            for flag in self.hallucination_flags:
                print(f"    - {flag}")
        
        if self.retrieval_metrics:
            print(f"\n🔍 RETRIEVAL METRICS:")
            print(f"  Similar Ideas Found: {self.retrieval_metrics.similar_ideas_count}")
            print(f"  Top Similarity Score: {self.retrieval_metrics.top_similarity_score:.1%}")
            print(f"  Average Similarity: {self.retrieval_metrics.avg_similarity_score:.1%}")
            print(f"  Retrieval Time: {self.retrieval_metrics.retrieval_time_ms:.0f}ms")
        
        if self.search_metrics:
            print(f"\n🌐 WEB SEARCH METRICS:")
            print(f"  Search Performed: {'Yes' if self.search_metrics.search_performed else 'No'}")
            print(f"  Queries Executed: {self.search_metrics.queries_count}")
            print(f"  Results Found: {self.search_metrics.results_found}")
            print(f"  Search Time: {self.search_metrics.search_time_ms:.0f}ms")
        
        print(f"\n🤖 AGENT METRICS:")
        for metrics in self.agent_metrics:
            print(f"  {metrics.agent_name}:")
            print(f"    Tokens: {metrics.tokens_used:,} | Time: {metrics.execution_time_ms:.0f}ms | Confidence: {metrics.confidence_score:.1%}")
        
        print("\n" + "="*80 + "\n")
    
    def save_to_file(self, filepath: str):
        """Save metrics to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.get_summary(), f, indent=2)


# Global instance
evaluation_tracker = EvaluationMetrics()
