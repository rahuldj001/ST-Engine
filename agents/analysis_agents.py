from typing import Dict, Any
from agents.base_agent import BaseAgent


class MarketAnalysisAgent(BaseAgent):
    """Agent specialized in market analysis"""
    
    def __init__(self):
        super().__init__(
            name="Market Analyst",
            role="Market research and analysis specialist"
        )
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Perform comprehensive market analysis
        
        Args:
            context: Analysis context with idea, plan, and market trends
            
        Returns:
            Detailed market analysis
        """
        idea = context.get("idea", "")
        plan = context.get("plan", "")
        market_trends = context.get("market_trends", "")
        similar_context = context.get("similar_ideas_context", "")
        
        prompt = self._build_prompt(
            """You are a market analysis expert specializing in startup feasibility.

Startup Idea: {idea}

Strategic Plan:
{plan}

Market Trends:
{market_trends}

{similar_context}

Provide a comprehensive market analysis covering:
1. Market size and growth potential
2. Market trends and dynamics
3. Market gaps and opportunities
4. Regulatory environment
5. Technology trends affecting the market
6. Customer pain points being addressed

Be specific, data-driven, and actionable.""",
            idea=idea,
            plan=plan,
            market_trends=market_trends,
            similar_context=similar_context
        )
        
        response = await self.llm.ainvoke(prompt)
        return response.content


class CompetitionAgent(BaseAgent):
    """Agent specialized in competitive analysis"""
    
    def __init__(self):
        super().__init__(
            name="Competition Analyst",
            role="Competitive intelligence specialist"
        )
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Analyze competition and market positioning
        
        Args:
            context: Analysis context
            
        Returns:
            Competition analysis
        """
        idea = context.get("idea", "")
        market_analysis = context.get("market_analysis", "")
        market_trends = context.get("market_trends", "")
        
        prompt = self._build_prompt(
            """You are a competitive intelligence expert.

Startup Idea: {idea}

Market Analysis:
{market_analysis}

Market Trends:
{market_trends}

Provide detailed competitive analysis:
1. Direct competitors (existing solutions)
2. Indirect competitors (alternative solutions)
3. Competitive advantages and differentiators
4. Barriers to entry
5. Competitive positioning strategy
6. Market share potential

Include specific company names and products where applicable.""",
            idea=idea,
            market_analysis=market_analysis,
            market_trends=market_trends
        )
        
        response = await self.llm.ainvoke(prompt)
        return response.content


class RevenueAgent(BaseAgent):
    """Agent specialized in revenue modeling"""
    
    def __init__(self):
        super().__init__(
            name="Revenue Strategist",
            role="Revenue model and monetization expert"
        )
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Design revenue model and monetization strategy
        
        Args:
            context: Analysis context
            
        Returns:
            Revenue model analysis
        """
        idea = context.get("idea", "")
        market_analysis = context.get("market_analysis", "")
        target_audience = context.get("target_audience", "")
        
        prompt = self._build_prompt(
            """You are a revenue modeling expert for startups.

Startup Idea: {idea}

Market Analysis:
{market_analysis}

Target Audience:
{target_audience}

Design a comprehensive revenue model:
1. Primary revenue streams
2. Pricing strategy and tiers
3. Customer acquisition economics (CAC, LTV)
4. Revenue projections (Year 1-3)
5. Monetization timeline
6. Alternative revenue opportunities
7. Unit economics

Be specific with numbers and realistic projections.""",
            idea=idea,
            market_analysis=market_analysis,
            target_audience=target_audience
        )
        
        response = await self.llm.ainvoke(prompt)
        return response.content
