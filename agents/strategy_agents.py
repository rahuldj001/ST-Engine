from typing import Dict, Any
from agents.base_agent import BaseAgent


class CostAgent(BaseAgent):
    """Agent specialized in cost structure analysis"""
    
    def __init__(self):
        super().__init__(
            name="Cost Analyst",
            role="Cost structure and financial planning expert"
        )
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Analyze cost structure and burn rate
        
        Args:
            context: Analysis context
            
        Returns:
            Cost structure analysis
        """
        idea = context.get("idea", "")
        revenue_model = context.get("revenue_model", "")
        market_analysis = context.get("market_analysis", "")
        
        prompt = self._build_prompt(
            """You are a financial planning expert for startups.

Startup Idea: {idea}

Revenue Model:
{revenue_model}

Market Analysis:
{market_analysis}

Provide detailed cost structure analysis:
1. Initial setup costs (one-time)
2. Fixed monthly costs (infrastructure, salaries, rent)
3. Variable costs (per customer/transaction)
4. Technology and development costs
5. Marketing and customer acquisition costs
6. Estimated burn rate (monthly)
7. Runway and funding requirements
8. Break-even analysis

Provide realistic numbers and ranges.""",
            idea=idea,
            revenue_model=revenue_model,
            market_analysis=market_analysis
        )
        
        response = await self.llm.ainvoke(prompt)
        return response.content


class GTMAgent(BaseAgent):
    """Agent specialized in go-to-market strategy"""
    
    def __init__(self):
        super().__init__(
            name="GTM Strategist",
            role="Go-to-market and growth expert"
        )
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Design go-to-market strategy
        
        Args:
            context: Analysis context
            
        Returns:
            GTM strategy
        """
        idea = context.get("idea", "")
        target_audience = context.get("target_audience", "")
        competition = context.get("competition_analysis", "")
        revenue_model = context.get("revenue_model", "")
        
        prompt = self._build_prompt(
            """You are a go-to-market strategy expert.

Startup Idea: {idea}

Target Audience:
{target_audience}

Competition Analysis:
{competition}

Revenue Model:
{revenue_model}

Design a comprehensive go-to-market strategy:
1. Launch strategy and timeline
2. Customer acquisition channels
3. Marketing and positioning strategy
4. Sales strategy (if applicable)
5. Partnership opportunities
6. Growth tactics and scaling plan
7. Key milestones (0-6 months, 6-12 months, 12-24 months)
8. Success metrics and KPIs

Be specific and actionable.""",
            idea=idea,
            target_audience=target_audience,
            competition=competition,
            revenue_model=revenue_model
        )
        
        response = await self.llm.ainvoke(prompt)
        return response.content


class TargetAudienceAgent(BaseAgent):
    """Agent specialized in target audience identification"""
    
    def __init__(self):
        super().__init__(
            name="Audience Analyst",
            role="Target audience and customer segmentation expert"
        )
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Identify and analyze target audience
        
        Args:
            context: Analysis context
            
        Returns:
            Target audience analysis
        """
        idea = context.get("idea", "")
        market_analysis = context.get("market_analysis", "")
        
        prompt = self._build_prompt(
            """You are a customer segmentation expert.

Startup Idea: {idea}

Market Analysis:
{market_analysis}

Identify and analyze the target audience:
1. Primary customer segments
2. Demographics (age, location, income, education)
3. Psychographics (behaviors, interests, values)
4. Customer pain points and needs
5. Buying behavior and decision factors
6. Customer personas (2-3 detailed personas)
7. Total addressable market size for each segment

Be specific and data-driven.""",
            idea=idea,
            market_analysis=market_analysis
        )
        
        response = await self.llm.ainvoke(prompt)
        return response.content
