import asyncio
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

if "langchain_groq" not in sys.modules:
    fake_mod = types.ModuleType("langchain_groq")

    class _FakeChatGroq:
        def __init__(self, *args, **kwargs):
            pass

        async def ainvoke(self, _prompt: str):
            return SimpleNamespace(content="")

    fake_mod.ChatGroq = _FakeChatGroq
    sys.modules["langchain_groq"] = fake_mod

if "dotenv" not in sys.modules:
    dotenv_mod = types.ModuleType("dotenv")
    dotenv_mod.load_dotenv = lambda *args, **kwargs: None
    sys.modules["dotenv"] = dotenv_mod

if "pydantic" not in sys.modules:
    pyd = types.ModuleType("pydantic")
    def Field(default=None, **kwargs):
        return default
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self):
            return self.__dict__.copy()
    pyd.Field = Field
    pyd.BaseModel = BaseModel
    sys.modules["pydantic"] = pyd


class _FakeLLM:
    def __init__(self, content: str):
        self._content = content

    async def ainvoke(self, _prompt: str):
        return SimpleNamespace(content=self._content)


class AgentRefactorTests(unittest.IsolatedAsyncioTestCase):
    async def test_market_intelligence_agent_parses_sections(self):
        from agents.base_agent import BaseAgent

        with patch.object(BaseAgent, "_initialize_llm", return_value=_FakeLLM("")):
            from agents.market_intelligence import MarketIntelligenceAgent

            agent = MarketIntelligenceAgent()
            agent.llm = _FakeLLM("MARKET_DEMAND: Strong demand\nAUDIENCE_PROFILE: SMB operators\nCOMPETITION_LANDSCAPE: Fragmented market\nSUMMARY: Good opportunity")
            out = await agent.execute({"idea": "AI copilot"})

            self.assertEqual(out["market_demand"], "Strong demand")
            self.assertEqual(out["audience_profile"], "SMB operators")
            self.assertEqual(out["competition_landscape"], "Fragmented market")
            self.assertEqual(out["summary"], "Good opportunity")

    async def test_financial_strategy_agent_parses_sections(self):
        from agents.base_agent import BaseAgent

        with patch.object(BaseAgent, "_initialize_llm", return_value=_FakeLLM("")):
            from agents.financial_strategy import FinancialStrategyAgent

            agent = FinancialStrategyAgent()
            agent.llm = _FakeLLM("REVENUE_MODEL: Subscription + usage\nCOST_STRUCTURE: Infra + payroll\nSUMMARY: Watch CAC")
            out = await agent.execute({"idea": "AI copilot"})

            self.assertEqual(out["revenue_model_summary"], "Subscription + usage")
            self.assertEqual(out["cost_structure_summary"], "Infra + payroll")
            self.assertEqual(out["summary"], "Watch CAC")

    async def test_orchestrator_combined_report_flow(self):
        # Stub heavy optional imports required by planner/rag path
        if "langchain_community" not in sys.modules:
            lc_mod = types.ModuleType("langchain_community")
            lc_tools = types.ModuleType("langchain_community.tools")

            class _FakeSearch:
                def run(self, *_a, **_k):
                    return ""

            lc_tools.DuckDuckGoSearchRun = _FakeSearch
            lc_mod.tools = lc_tools
            sys.modules["langchain_community"] = lc_mod
            sys.modules["langchain_community.tools"] = lc_tools

        if "sentence_transformers" not in sys.modules:
            st_mod = types.ModuleType("sentence_transformers")

            class _FakeSentenceTransformer:
                def __init__(self, *args, **kwargs):
                    pass

                def encode(self, texts):
                    if isinstance(texts, list):
                        return [[0.0] * 3 for _ in texts]
                    return [0.0] * 3

            st_mod.SentenceTransformer = _FakeSentenceTransformer
            sys.modules["sentence_transformers"] = st_mod

        if "supabase" not in sys.modules:
            supa = types.ModuleType("supabase")
            supa.create_client = lambda *args, **kwargs: object()
            supa.Client = object
            sys.modules["supabase"] = supa

        import os
        os.environ.setdefault("SUPABASE_URL", "http://example.com")
        os.environ.setdefault("SUPABASE_KEY", "test")

        from agents.base_agent import BaseAgent

        with patch.object(BaseAgent, "_initialize_llm", return_value=_FakeLLM("")):
            from agents.orchestrator import AgentOrchestrator
            import agents.orchestrator as orch_module

            orchestrator = AgentOrchestrator()

            async def fake_market(_context):
                await asyncio.sleep(0.02)
                return {
                    "market_demand": "Demand",
                    "audience_profile": "Audience",
                    "competition_landscape": "Competition",
                    "summary": "Summary",
                    "full_output": "full market",
                }

            async def fake_financial(_context):
                await asyncio.sleep(0.02)
                return {
                    "revenue_model_summary": "Revenue",
                    "cost_structure_summary": "Cost",
                    "summary": "Financial summary",
                    "full_output": "full financial",
                }

            async def fake_gtm(_context):
                await asyncio.sleep(0.02)
                return "GTM plan"

            async def fake_success(_context):
                return {"success_probability": 70.0, "best_location": "Berlin", "reasoning": "Looks viable"}

            async def fake_critic(context):
                report = context["full_report"]
                assert all(k in report for k in ["market_intelligence", "financial_strategy", "go_to_market", "critique"])
                return "Critique output"

            orchestrator.planner.execute = AsyncMock(return_value="Plan")
            orchestrator.market_intelligence_agent.execute = fake_market
            orchestrator.financial_strategy_agent.execute = fake_financial
            orchestrator.gtm_strategist.execute = fake_gtm
            orchestrator.success_analyst.execute = fake_success
            orchestrator.critic.execute = fake_critic

            orch_module.rag_service.retrieve_similar_ideas = AsyncMock(return_value=[])
            orch_module.rag_service.build_context_from_similar_ideas = lambda _x: ""
            orch_module.rag_service.store_idea_with_report = AsyncMock(return_value=None)

            et = orch_module.evaluation_tracker
            et.reset = lambda: None
            et.start_tracking = lambda: None
            et.set_retrieval_metrics = lambda *_a, **_k: None
            et.set_search_metrics = lambda *_a, **_k: None
            et.add_agent_metrics = lambda *_a, **_k: None
            et.calculate_overall_confidence = lambda: 0.0
            et.assess_hallucination_risk = lambda: "low"
            et.end_tracking = lambda: None
            et.get_summary = lambda: {}
            et.print_summary = lambda: None
            et.retrieval_metrics = None

            orch_module.HallucinationDetector.generate_hallucination_report = staticmethod(lambda **_k: {})
            orch_module.HallucinationDetector.print_hallucination_report = staticmethod(lambda _r: None)

            response = await orchestrator.analyze_startup_idea("Idea", "SaaS", "EU")

            self.assertEqual(response.report.market_analysis, "Demand")
            self.assertEqual(response.report.target_audience, "Audience")
            self.assertEqual(response.report.competition_analysis, "Competition")
            self.assertEqual(response.report.revenue_model, "Revenue")
            self.assertEqual(response.report.cost_structure, "Cost")
            self.assertEqual(response.report.go_to_market, "GTM plan")
            self.assertEqual(response.critique, "Critique output")


if __name__ == "__main__":
    unittest.main()
