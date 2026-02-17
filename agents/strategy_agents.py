from typing import Any, Dict

from agents.base_agent import BaseAgent


class GTMAgent(BaseAgent):
    """Agent specialized in go-to-market strategy"""

    def __init__(self):
        super().__init__(
            name="GTM Strategist",
            role="Go-to-market and growth expert"
        )

    async def execute(self, context: Dict[str, Any]) -> str:
        """Design go-to-market strategy."""
        idea = context.get("idea", "")
        audience = context.get("audience_profile", context.get("target_audience", ""))
        competition = context.get("competition_landscape", context.get("competition_analysis", ""))
        finance = context.get("financial_strategy", context.get("revenue_model", ""))

        prompt = self._build_prompt(
            """You are a startup GTM expert.

Idea: {idea}
Audience: {audience}
Competition: {competition}
Financial strategy: {finance}

Provide concise GTM plan:
1) Launch sequence (0-3, 3-12, 12-24 months)
2) Acquisition channels + core messaging
3) Sales/partnership motion
4) Key metrics and milestones
5) Biggest GTM risks + mitigations

Keep it actionable and short.""",
            idea=idea,
            audience=audience[:900],
            competition=competition[:900],
            finance=finance[:900],
        )

        response = await self.llm.ainvoke(prompt)
        return response.content
