from typing import Any, Dict

from agents.base_agent import BaseAgent


class FinancialStrategyAgent(BaseAgent):
    """Unified agent for revenue model and cost structure."""

    def __init__(self):
        super().__init__(
            name="Financial Strategist",
            role="Revenue and cost planning specialist",
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, str]:
        idea = context.get("idea", "")
        plan = context.get("plan", "")
        market_trends = context.get("market_trends", "")
        target_market = context.get("target_market", "global")
        industry = context.get("industry", "general")
        similar_context = context.get("similar_ideas_context", "")

        prompt = self._build_prompt(
            """You design startup financial strategy.

Idea: {idea}
Industry: {industry}
Target market: {target_market}
Plan: {plan}
Trends: {market_trends}
Related context: {similar_context}

Return concise sections:
1) REVENUE_MODEL: core streams, pricing logic, simple 12-36 month trajectory.
2) COST_STRUCTURE: fixed + variable costs, burn-rate drivers, break-even path.
3) SUMMARY: 3-5 bullets with major financial risks and mitigation.

Keep numbers realistic and concise.""",
            idea=idea,
            industry=industry,
            target_market=target_market,
            plan=plan[:700],
            market_trends=market_trends[:700],
            similar_context=similar_context[:600],
        )

        response = await self.llm.ainvoke(prompt)
        content = response.content

        return {
            "revenue_model_summary": self._extract_section(content, "REVENUE_MODEL"),
            "cost_structure_summary": self._extract_section(content, "COST_STRUCTURE"),
            "summary": self._extract_section(content, "SUMMARY"),
            "full_output": content,
        }

    @staticmethod
    def _extract_section(content: str, header: str) -> str:
        marker = f"{header}:"
        if marker not in content:
            return ""

        section = content.split(marker, 1)[1]
        for next_header in ["REVENUE_MODEL:", "COST_STRUCTURE:", "SUMMARY:"]:
            if next_header == marker:
                continue
            if next_header in section:
                section = section.split(next_header, 1)[0]
        return section.strip()
