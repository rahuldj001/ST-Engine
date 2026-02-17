from typing import Dict, Any, Tuple
import asyncio
import time

from agents import (
    PlannerAgent,
    MarketIntelligenceAgent,
    FinancialStrategyAgent,
    GTMAgent,
    SuccessProbabilityAgent,
    CriticAgent,
)
from rag.retrieval import rag_service
from models.schemas import FeasibilityReport, FeasibilityResponse
from evaluation.metrics import evaluation_tracker
from evaluation.confidence import ConfidenceScorer
from evaluation.hallucination import HallucinationDetector


class AgentOrchestrator:
    """Orchestrates the multi-agent workflow for feasibility analysis with evaluation tracking"""

    def __init__(self):
        self.planner = PlannerAgent()
        self.market_intelligence_agent = MarketIntelligenceAgent()
        self.financial_strategy_agent = FinancialStrategyAgent()
        self.gtm_strategist = GTMAgent()
        self.success_analyst = SuccessProbabilityAgent()
        self.critic = CriticAgent()

    async def _timed_execute(self, label: str, coro) -> Tuple[str, Any, float]:
        start = time.time()
        result = await coro
        duration_ms = (time.time() - start) * 1000
        return label, result, duration_ms

    async def analyze_startup_idea(
        self,
        idea: str,
        industry: str = "general",
        target_market: str = "global"
    ) -> FeasibilityResponse:
        evaluation_tracker.reset()
        evaluation_tracker.start_tracking()

        print("Retrieving similar ideas from database...")
        retrieval_start = time.time()
        similar_ideas = await rag_service.retrieve_similar_ideas(idea)
        retrieval_time_ms = (time.time() - retrieval_start) * 1000
        similar_context = rag_service.build_context_from_similar_ideas(similar_ideas)
        evaluation_tracker.set_retrieval_metrics(similar_ideas, retrieval_time_ms)

        context: Dict[str, Any] = {
            "idea": idea,
            "industry": industry,
            "target_market": target_market,
            "similar_ideas_context": similar_context,
            "similar_ideas": similar_ideas,
        }

        print("Planning analysis strategy...")
        planner_start = time.time()
        context["plan"] = await self.planner.execute(context)
        planner_time_ms = (time.time() - planner_start) * 1000

        planner_confidence = ConfidenceScorer.calculate_planner_confidence(
            context["plan"],
            industry_extracted=context.get("extracted_industry") is not None,
            location_extracted=context.get("extracted_location") is not None,
            search_performed=context.get("search_decision", {}).get("search_needed", False),
            search_results_count=len(context.get("search_results", [])),
        )
        evaluation_tracker.add_agent_metrics(
            "Planner",
            ConfidenceScorer.estimate_tokens(context["plan"]),
            planner_time_ms,
            planner_confidence,
        )

        search_decision = context.get("search_decision", {})
        evaluation_tracker.set_search_metrics(
            search_performed=search_decision.get("search_needed", False),
            queries=search_decision.get("queries", []),
            results=context.get("search_results", []),
            search_time_ms=planner_time_ms * 0.3,
        )

        print("Running core agents in parallel...")
        parallel_results = await asyncio.gather(
            self._timed_execute("market_intelligence", self.market_intelligence_agent.execute(context)),
            self._timed_execute("financial_strategy", self.financial_strategy_agent.execute(context)),
            self._timed_execute("go_to_market", self.gtm_strategist.execute(context)),
        )

        for label, result, duration in parallel_results:
            context[label] = result
            confidence = ConfidenceScorer.calculate_analysis_confidence(
                result["full_output"] if isinstance(result, dict) and "full_output" in result else str(result),
                plan_available=True,
                market_trends_available=bool(context.get("market_trends")),
                similar_ideas_count=len(similar_ideas),
            )
            tokens = ConfidenceScorer.estimate_tokens(
                result["full_output"] if isinstance(result, dict) and "full_output" in result else str(result)
            )
            evaluation_tracker.add_agent_metrics(label.replace("_", " ").title(), tokens, duration, confidence)

        market_intelligence = context["market_intelligence"]
        financial_strategy = context["financial_strategy"]

        # Keep legacy fields for downstream compatibility and response schema
        context["market_analysis"] = market_intelligence.get("market_demand") or market_intelligence.get("full_output", "")
        context["target_audience"] = market_intelligence.get("audience_profile", "")
        context["competition_analysis"] = market_intelligence.get("competition_landscape", "")
        context["revenue_model"] = financial_strategy.get("revenue_model_summary") or financial_strategy.get("full_output", "")
        context["cost_structure"] = financial_strategy.get("cost_structure_summary", "")
        context["go_to_market"] = context["go_to_market"] if isinstance(context["go_to_market"], str) else str(context["go_to_market"])

        # Feed richer context after market intelligence exists
        context["financial_strategy"] = financial_strategy.get("full_output", "")
        context["audience_profile"] = context["target_audience"]
        context["competition_landscape"] = context["competition_analysis"]

        print("Calculating success probability...")
        success_start = time.time()
        success_data = await self.success_analyst.execute(context)
        success_time_ms = (time.time() - success_start) * 1000
        context["success_probability"] = success_data["success_probability"]
        context["best_location"] = success_data["best_location"]
        evaluation_tracker.add_agent_metrics(
            "Success Probability Analyst",
            ConfidenceScorer.estimate_tokens(success_data["reasoning"]),
            success_time_ms,
            ConfidenceScorer.calculate_analysis_confidence(
                success_data["reasoning"],
                plan_available=True,
                market_trends_available=bool(context.get("market_trends")),
                similar_ideas_count=len(similar_ideas),
            ),
        )

        combined_report = {
            "market_intelligence": market_intelligence,
            "financial_strategy": financial_strategy,
            "go_to_market": context["go_to_market"],
            "critique": "",
            # legacy keys consumed by critic internals
            "market_analysis": context["market_analysis"],
            "target_audience": context["target_audience"],
            "competition_analysis": context["competition_analysis"],
            "revenue_model": context["revenue_model"],
            "cost_structure": context["cost_structure"],
            "success_probability": context["success_probability"],
            "best_location": context["best_location"],
        }

        print("Reviewing report quality...")
        critic_start = time.time()
        context["full_report"] = combined_report
        critique = await self.critic.execute(context)
        critic_time_ms = (time.time() - critic_start) * 1000
        combined_report["critique"] = critique

        evaluation_tracker.add_agent_metrics(
            "Critic",
            ConfidenceScorer.estimate_tokens(critique),
            critic_time_ms,
            ConfidenceScorer.calculate_critic_confidence(
                critique,
                revenue_issues_found=context.get("probability_adjustment", 0) > 0,
                competition_issues_found=context.get("probability_adjustment", 0) > 0,
                adjustment_made=context.get("adjusted_success_probability") is not None,
            ),
        )

        if context.get("adjusted_success_probability") is not None:
            context["success_probability"] = context["adjusted_success_probability"]

        report = FeasibilityReport(
            market_analysis=context["market_analysis"],
            target_audience=context["target_audience"],
            revenue_model=context["revenue_model"],
            competition_analysis=context["competition_analysis"],
            cost_structure=context["cost_structure"],
            go_to_market=context["go_to_market"],
            success_probability=context["success_probability"],
            best_location=context["best_location"],
        )

        print("Calculating evaluation metrics...")
        _ = evaluation_tracker.calculate_overall_confidence()
        _ = evaluation_tracker.assess_hallucination_risk()

        hallucination_report = HallucinationDetector.generate_hallucination_report(
            search_performed=context.get("search_decision", {}).get("search_needed", False),
            search_results_count=len(context.get("search_results", [])),
            similar_ideas_count=len(similar_ideas),
            top_similarity_score=evaluation_tracker.retrieval_metrics.top_similarity_score if evaluation_tracker.retrieval_metrics else 0.0,
            market_analysis=context.get("market_analysis", ""),
            competition_analysis=context.get("competition_analysis", ""),
            revenue_model=context.get("revenue_model", ""),
        )

        evaluation_tracker.end_tracking()

        print("Storing report in database...")
        await rag_service.store_idea_with_report(idea, report.model_dump())

        sources_used = [r["query"] for r in context.get("search_results", [])] if context.get("search_results") else []
        similar_idea_descriptions = [item.get("idea", "")[:100] + "..." for item in similar_ideas[:3]]
        evaluation_summary = evaluation_tracker.get_summary()

        evaluation_tracker.print_summary()
        HallucinationDetector.print_hallucination_report(hallucination_report)

        response = FeasibilityResponse(
            idea=idea,
            report=report,
            similar_ideas=similar_idea_descriptions,
            sources_used=sources_used,
            critique=critique,
            evaluation_metrics=evaluation_summary,
            hallucination_report=hallucination_report,
        )

        print("Analysis complete!")
        return response


orchestrator = AgentOrchestrator()
