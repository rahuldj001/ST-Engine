from typing import Any, Dict

from agents.base_agent import BaseAgent


class MarketIntelligenceAgent(BaseAgent):
    """Unified agent for market demand, audience, and competition insights."""

    def __init__(self):
        super().__init__(
            name="Market Intelligence Analyst",
            role="Market demand, audience, and competition specialist",
        )

    async def execute(self, context: Dict[str, Any]) -> Dict[str, str]:
        idea = context.get("idea", "")
        plan = context.get("plan", "")
        market_trends = context.get("market_trends", "")
        similar_context = context.get("similar_ideas_context", "")

        prompt = self._build_prompt(
            """You analyze startup markets.

Idea: {idea}
Plan: {plan}
Trends: {market_trends}
{similar_context}

Return concise sections:
1) MARKET_DEMAND: size, growth, urgent pain points.
2) AUDIENCE_PROFILE: top segments, behavior, buying triggers.
3) COMPETITION_LANDSCAPE: direct/indirect competitors, differentiation gaps.
4) SUMMARY: 4-6 bullets with key opportunities and risks.

Use practical assumptions and avoid filler.""",
            idea=idea,
            plan=plan[:1000],
            market_trends=market_trends[:1000],
            similar_context=similar_context[:1200],
        )

        response = await self.llm.ainvoke(prompt)
        content = response.content

        return {
            "market_demand": self._extract_section(content, "MARKET_DEMAND"),
            "audience_profile": self._extract_section(content, "AUDIENCE_PROFILE"),
            "competition_landscape": self._extract_section(content, "COMPETITION_LANDSCAPE"),
            "summary": self._extract_section(content, "SUMMARY"),
            "full_output": content,
        }

    @staticmethod
    def _extract_section(content: str, header: str) -> str:
        marker = f"{header}:"
        if marker not in content:
            return ""

        section = content.split(marker, 1)[1]
        for next_header in [
            "MARKET_DEMAND:",
            "AUDIENCE_PROFILE:",
            "COMPETITION_LANDSCAPE:",
            "SUMMARY:",
        ]:
            if next_header == marker:
                continue
            if next_header in section:
                section = section.split(next_header, 1)[0]
        return section.strip()
