from typing import Dict, Any
import time
from agents import (
    PlannerAgent,
    MarketAnalysisAgent,
    CompetitionAgent,
    RevenueAgent,
    CostAgent,
    GTMAgent,
    TargetAudienceAgent,
    SuccessProbabilityAgent,
    CriticAgent
)
from rag.retrieval import rag_service
from models.schemas import FeasibilityReport, FeasibilityResponse
from evaluation.metrics import evaluation_tracker
from evaluation.confidence import ConfidenceScorer
from evaluation.hallucination import HallucinationDetector


class AgentOrchestrator:
    """Orchestrates the multi-agent workflow for feasibility analysis with evaluation tracking"""
    
    def __init__(self):
        # Initialize all agents
        self.planner = PlannerAgent()
        self.market_analyst = MarketAnalysisAgent()
        self.competition_analyst = CompetitionAgent()
        self.revenue_strategist = RevenueAgent()
        self.cost_analyst = CostAgent()
        self.gtm_strategist = GTMAgent()
        self.audience_analyst = TargetAudienceAgent()
        self.success_analyst = SuccessProbabilityAgent()
        self.critic = CriticAgent()
    
    async def analyze_startup_idea(
        self,
        idea: str,
        industry: str = "general",
        target_market: str = "global"
    ) -> FeasibilityResponse:
        """
        Orchestrate the complete feasibility analysis workflow with evaluation tracking
        
        Args:
            idea: The startup idea to analyze
            industry: Industry sector
            target_market: Target market or geography
            
        Returns:
            Complete feasibility response with report, metadata, and evaluation metrics
        """
        # Reset and start evaluation tracking
        evaluation_tracker.reset()
        evaluation_tracker.start_tracking()
        
        # Step 1: Retrieve similar ideas from RAG
        print("Retrieving similar ideas from database...")
        retrieval_start = time.time()
        similar_ideas = await rag_service.retrieve_similar_ideas(idea)
        retrieval_time_ms = (time.time() - retrieval_start) * 1000
        similar_context = rag_service.build_context_from_similar_ideas(similar_ideas)
        
        # Track retrieval metrics
        evaluation_tracker.set_retrieval_metrics(similar_ideas, retrieval_time_ms)
        
        # Initialize context
        context: Dict[str, Any] = {
            "idea": idea,
            "industry": industry,
            "target_market": target_market,
            "similar_ideas_context": similar_context,
            "similar_ideas": similar_ideas
        }
        
        # Step 2: Planner creates strategy and gathers market trends
        print("Planning analysis strategy...")
        planner_start = time.time()
        context["plan"] = await self.planner.execute(context)
        planner_time_ms = (time.time() - planner_start) * 1000
        
        # Calculate planner confidence
        planner_confidence = ConfidenceScorer.calculate_planner_confidence(
            context["plan"],
            industry_extracted=context.get("extracted_industry") is not None,
            location_extracted=context.get("extracted_location") is not None,
            search_performed=context.get("search_decision", {}).get("search_needed", False),
            search_results_count=len(context.get("search_results", []))
        )
        
        # Track planner metrics
        planner_tokens = ConfidenceScorer.estimate_tokens(context["plan"])
        evaluation_tracker.add_agent_metrics("Planner", planner_tokens, planner_time_ms, planner_confidence)
        
        # Track search metrics
        search_decision = context.get("search_decision", {})
        evaluation_tracker.set_search_metrics(
            search_performed=search_decision.get("search_needed", False),
            queries=search_decision.get("queries", []),
            results=context.get("search_results", []),
            search_time_ms=planner_time_ms * 0.3  # Rough estimate of search portion
        )
        
        # Step 3: Market analysis
        print("Analyzing market...")
        market_start = time.time()
        context["market_analysis"] = await self.market_analyst.execute(context)
        market_time_ms = (time.time() - market_start) * 1000
        
        market_confidence = ConfidenceScorer.calculate_analysis_confidence(
            context["market_analysis"],
            plan_available=True,
            market_trends_available=bool(context.get("market_trends")),
            similar_ideas_count=len(similar_ideas)
        )
        market_tokens = ConfidenceScorer.estimate_tokens(context["market_analysis"])
        evaluation_tracker.add_agent_metrics("Market Analyst", market_tokens, market_time_ms, market_confidence)
        
        # Step 4: Target audience identification
        print("Identifying target audience...")
        audience_start = time.time()
        context["target_audience"] = await self.audience_analyst.execute(context)
        audience_time_ms = (time.time() - audience_start) * 1000
        
        audience_confidence = ConfidenceScorer.calculate_analysis_confidence(
            context["target_audience"],
            plan_available=True,
            market_trends_available=bool(context.get("market_trends")),
            similar_ideas_count=len(similar_ideas)
        )
        audience_tokens = ConfidenceScorer.estimate_tokens(context["target_audience"])
        evaluation_tracker.add_agent_metrics("Audience Analyst", audience_tokens, audience_time_ms, audience_confidence)
        
        # Step 5: Competition analysis
        print("Analyzing competition...")
        competition_start = time.time()
        context["competition_analysis"] = await self.competition_analyst.execute(context)
        competition_time_ms = (time.time() - competition_start) * 1000
        
        competition_confidence = ConfidenceScorer.calculate_analysis_confidence(
            context["competition_analysis"],
            plan_available=True,
            market_trends_available=bool(context.get("market_trends")),
            similar_ideas_count=len(similar_ideas)
        )
        competition_tokens = ConfidenceScorer.estimate_tokens(context["competition_analysis"])
        evaluation_tracker.add_agent_metrics("Competition Analyst", competition_tokens, competition_time_ms, competition_confidence)
        
        # Step 6: Revenue model design
        print("Designing revenue model...")
        revenue_start = time.time()
        context["revenue_model"] = await self.revenue_strategist.execute(context)
        revenue_time_ms = (time.time() - revenue_start) * 1000
        
        revenue_confidence = ConfidenceScorer.calculate_analysis_confidence(
            context["revenue_model"],
            plan_available=True,
            market_trends_available=bool(context.get("market_trends")),
            similar_ideas_count=len(similar_ideas)
        )
        revenue_tokens = ConfidenceScorer.estimate_tokens(context["revenue_model"])
        evaluation_tracker.add_agent_metrics("Revenue Strategist", revenue_tokens, revenue_time_ms, revenue_confidence)
        
        # Step 7: Cost structure analysis
        print("Analyzing cost structure...")
        cost_start = time.time()
        context["cost_structure"] = await self.cost_analyst.execute(context)
        cost_time_ms = (time.time() - cost_start) * 1000
        
        cost_confidence = ConfidenceScorer.calculate_analysis_confidence(
            context["cost_structure"],
            plan_available=True,
            market_trends_available=bool(context.get("market_trends")),
            similar_ideas_count=len(similar_ideas)
        )
        cost_tokens = ConfidenceScorer.estimate_tokens(context["cost_structure"])
        evaluation_tracker.add_agent_metrics("Cost Analyst", cost_tokens, cost_time_ms, cost_confidence)
        
        # Step 8: Go-to-market strategy
        print("Creating GTM strategy...")
        gtm_start = time.time()
        context["go_to_market"] = await self.gtm_strategist.execute(context)
        gtm_time_ms = (time.time() - gtm_start) * 1000
        
        gtm_confidence = ConfidenceScorer.calculate_analysis_confidence(
            context["go_to_market"],
            plan_available=True,
            market_trends_available=bool(context.get("market_trends")),
            similar_ideas_count=len(similar_ideas)
        )
        gtm_tokens = ConfidenceScorer.estimate_tokens(context["go_to_market"])
        evaluation_tracker.add_agent_metrics("GTM Strategist", gtm_tokens, gtm_time_ms, gtm_confidence)
        
        # Step 9: Success probability and location
        print("Calculating success probability...")
        success_start = time.time()
        success_data = await self.success_analyst.execute(context)
        success_time_ms = (time.time() - success_start) * 1000
        context["success_probability"] = success_data["success_probability"]
        context["best_location"] = success_data["best_location"]
        
        success_confidence = ConfidenceScorer.calculate_analysis_confidence(
            success_data["reasoning"],
            plan_available=True,
            market_trends_available=bool(context.get("market_trends")),
            similar_ideas_count=len(similar_ideas)
        )
        success_tokens = ConfidenceScorer.estimate_tokens(success_data["reasoning"])
        evaluation_tracker.add_agent_metrics("Success Probability Analyst", success_tokens, success_time_ms, success_confidence)
        
        # Step 10: Create structured report (initial version)
        report = FeasibilityReport(
            market_analysis=context["market_analysis"],
            target_audience=context["target_audience"],
            revenue_model=context["revenue_model"],
            competition_analysis=context["competition_analysis"],
            cost_structure=context["cost_structure"],
            go_to_market=context["go_to_market"],
            success_probability=context["success_probability"],
            best_location=context["best_location"]
        )
        
        # Step 11: Critic reviews the report and adjusts success probability
        print("Reviewing report quality...")
        critic_start = time.time()
        context["full_report"] = report.model_dump()
        critique = await self.critic.execute(context)
        critic_time_ms = (time.time() - critic_start) * 1000
        
        # Calculate critic confidence
        critic_confidence = ConfidenceScorer.calculate_critic_confidence(
            critique,
            revenue_issues_found=context.get("probability_adjustment", 0) > 0,
            competition_issues_found=context.get("probability_adjustment", 0) > 0,
            adjustment_made=context.get("adjusted_success_probability") is not None
        )
        critic_tokens = ConfidenceScorer.estimate_tokens(critique)
        evaluation_tracker.add_agent_metrics("Critic", critic_tokens, critic_time_ms, critic_confidence)
        
        # Step 12: Update report with adjusted success probability if critic made adjustments
        if context.get("adjusted_success_probability") is not None:
            adjusted_prob = context["adjusted_success_probability"]
            print(f"  Updating success probability to adjusted value: {adjusted_prob}%")
            
            # Create updated report with adjusted probability
            report = FeasibilityReport(
                market_analysis=context["market_analysis"],
                target_audience=context["target_audience"],
                revenue_model=context["revenue_model"],
                competition_analysis=context["competition_analysis"],
                cost_structure=context["cost_structure"],
                go_to_market=context["go_to_market"],
                success_probability=adjusted_prob,  # Use adjusted value
                best_location=context["best_location"]
            )
        
        # Step 13: Calculate evaluation metrics
        print("Calculating evaluation metrics...")
        
        # Calculate overall confidence
        overall_confidence = evaluation_tracker.calculate_overall_confidence()
        
        # Assess hallucination risk
        hallucination_risk = evaluation_tracker.assess_hallucination_risk()
        
        # Generate detailed hallucination report
        hallucination_report = HallucinationDetector.generate_hallucination_report(
            search_performed=context.get("search_decision", {}).get("search_needed", False),
            search_results_count=len(context.get("search_results", [])),
            similar_ideas_count=len(similar_ideas),
            top_similarity_score=evaluation_tracker.retrieval_metrics.top_similarity_score if evaluation_tracker.retrieval_metrics else 0.0,
            market_analysis=context.get("market_analysis", ""),
            competition_analysis=context.get("competition_analysis", ""),
            revenue_model=context.get("revenue_model", "")
        )
        
        # End tracking
        evaluation_tracker.end_tracking()
        
        # Step 14: Store the final report in RAG database
        print("Storing report in database...")
        await rag_service.store_idea_with_report(idea, report.model_dump())
        
        # Compile sources used
        sources_used = []
        if context.get("search_results"):
            sources_used = [r["query"] for r in context["search_results"]]
        
        # Extract similar idea descriptions
        similar_idea_descriptions = [
            item.get("idea", "")[:100] + "..."
            for item in similar_ideas[:3]
        ]
        
        # Get evaluation summary
        evaluation_summary = evaluation_tracker.get_summary()
        
        # Print evaluation metrics
        evaluation_tracker.print_summary()
        HallucinationDetector.print_hallucination_report(hallucination_report)
        
        # Create response with evaluation data
        response = FeasibilityResponse(
    idea=idea,
    report=report,
    similar_ideas=similar_idea_descriptions,
    sources_used=sources_used,
    critique=critique,
    evaluation_metrics=evaluation_summary,
    hallucination_report=hallucination_report
)

        
        # Add evaluation metadata to response (as additional attributes)
       
        
        print("Analysis complete!")
        return response


# Global instance
orchestrator = AgentOrchestrator()

