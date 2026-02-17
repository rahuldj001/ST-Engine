from typing import Dict, Any, Optional
import re
from agents.base_agent import BaseAgent
from tools.web_search import web_search_tool


class PlannerAgent(BaseAgent):
    """Enhanced planner agent with intelligent extraction and conditional web search"""
    
    def __init__(self):
        super().__init__(
            name="Planner",
            role="Strategic planner and orchestrator"
        )
    
    async def _extract_industry_and_location(self, idea: str, industry: Optional[str], target_market: Optional[str]) -> Dict[str, str]:
        """
        Extract industry type and geographic location from the idea using LLM
        
        Args:
            idea: The startup idea
            industry: Provided industry (if any)
            target_market: Provided target market (if any)
            
        Returns:
            Dictionary with extracted industry and location
        """
        # If both are provided, return them
        if industry and industry != "general" and target_market and target_market != "global":
            return {"industry": industry, "location": target_market}
        
        extraction_prompt = f"""Analyze this startup idea and extract key information:

Startup Idea: {idea}

Extract and provide ONLY the following in this exact format:
INDUSTRY: [specific industry/sector, e.g., "fintech", "healthtech", "e-commerce", "SaaS", "edtech"]
LOCATION: [geographic market, e.g., "United States", "Europe", "Southeast Asia", "Global"]

If the idea doesn't specify a location, infer the most likely target market based on the idea.
If the industry is unclear, categorize it based on the core business model.

Be specific and concise. One or two words for industry, one region for location."""

        response = await self.llm.ainvoke(extraction_prompt)
        content = response.content
        
        # Parse the response
        extracted_industry = industry if industry and industry != "general" else "general"
        extracted_location = target_market if target_market and target_market != "global" else "global"
        
        try:
            lines = content.split('\n')
            for line in lines:
                if line.startswith("INDUSTRY:"):
                    extracted_industry = line.split(":", 1)[1].strip()
                elif line.startswith("LOCATION:"):
                    extracted_location = line.split(":", 1)[1].strip()
        except Exception as e:
            print(f"Error parsing extraction response: {e}")
        
        return {
            "industry": extracted_industry,
            "location": extracted_location
        }
    
    async def _decide_web_search(self, idea: str, industry: str, similar_context: str) -> Dict[str, Any]:
        """
        Intelligently decide whether to perform web search based on idea complexity
        
        Args:
            idea: The startup idea
            industry: Extracted industry
            similar_context: Context from similar ideas
            
        Returns:
            Dictionary with decision and reasoning
        """
        decision_prompt = f"""You are a research strategist. Decide if web search is needed for this startup analysis.

Startup Idea: {idea}
Industry: {industry}

Similar Ideas Context Available: {"Yes" if similar_context else "No"}

Decide if live web search is NECESSARY based on:
1. Is this a rapidly evolving industry? (AI, crypto, emerging tech = YES)
2. Are market trends critical to validation? (market-dependent ideas = YES)
3. Is the idea time-sensitive or trend-based? (YES)
4. Do we have sufficient similar context? (If yes = MAYBE NO)

Respond in this EXACT format:
SEARCH_NEEDED: [YES/NO]
REASON: [one sentence explaining why]
SEARCH_QUERIES: [comma-separated list of 2-3 specific search queries, or "NONE"]"""

        response = await self.llm.ainvoke(decision_prompt)
        content = response.content
        
        # Default to performing search
        search_needed = True
        reason = "Market research required"
        search_queries = []
        
        try:
            lines = content.split('\n')
            for line in lines:
                if line.startswith("SEARCH_NEEDED:"):
                    search_needed = "YES" in line.upper()
                elif line.startswith("REASON:"):
                    reason = line.split(":", 1)[1].strip()
                elif line.startswith("SEARCH_QUERIES:"):
                    queries_str = line.split(":", 1)[1].strip()
                    if queries_str != "NONE":
                        search_queries = [q.strip() for q in queries_str.split(",")]
        except Exception as e:
            print(f"Error parsing search decision: {e}")
        
        return {
            "search_needed": search_needed,
            "reason": reason,
            "queries": search_queries
        }
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Create an analysis plan with intelligent extraction and conditional web search
        
        Args:
            context: Dictionary containing 'idea', 'industry', 'target_market', 'similar_ideas_context'
            
        Returns:
            Analysis plan and structured context
        """
        idea = context.get("idea", "")
        industry = context.get("industry", "general")
        target_market = context.get("target_market", "global")
        similar_context = context.get("similar_ideas_context", "")
        
        # Step 1: Extract industry and location if not provided or generic
        print("  Extracting industry and location...")
        extraction = await self._extract_industry_and_location(idea, industry, target_market)
        extracted_industry = extraction["industry"]
        extracted_location = extraction["location"]
        
        # Update context with extracted information
        context["extracted_industry"] = extracted_industry
        context["extracted_location"] = extracted_location
        
        print(f"  Industry: {extracted_industry} | Location: {extracted_location}")
        
        # Step 2: Decide whether to perform web search
        print("  Deciding on web search necessity...")
        search_decision = await self._decide_web_search(idea, extracted_industry, similar_context)
        
        market_trends = ""
        search_results = []
        
        if search_decision["search_needed"]:
            print(f"  Web search needed: {search_decision['reason']}")
            
            # Use LLM-suggested queries or fall back to defaults
            if search_decision["queries"]:
                search_queries = search_decision["queries"]
            else:
                search_queries = [
                    f"{extracted_industry} market trends 2026",
                    f"{idea[:100]} market analysis",
                    f"startup opportunities in {extracted_location}"
                ]
            
            print(f"  Performing {len(search_queries)} searches...")
            search_results = web_search_tool.multi_search(search_queries)
            
            # Compile search results
            market_trends = "\n\n".join([
                f"Query: {r['query']}\nResults: {r['results'][:500]}"
                for r in search_results if r.get('results')
            ])
        else:
            print(f"  Skipping web search: {search_decision['reason']}")
            market_trends = "Web search skipped - sufficient context from similar ideas."
        
        # Step 3: Create structured context for execution agents
        structured_context = {
            "industry_type": extracted_industry,
            "geographic_location": extracted_location,
            "market_trends_available": bool(market_trends),
            "similar_ideas_available": bool(similar_context),
            "web_search_performed": search_decision["search_needed"],
            "key_focus_areas": []
        }
        
        # Step 4: Generate comprehensive analysis plan
        prompt = self._build_prompt(
            """You are a strategic planner for startup feasibility analysis.

Startup Idea: {idea}

EXTRACTED CONTEXT:
- Industry: {industry}
- Geographic Location: {location}
- Web Search Performed: {web_search}

{similar_context}

{market_trends_section}

Create a comprehensive analysis plan that provides STRUCTURED GUIDANCE for execution agents:

1. KEY FOCUS AREAS:
   - List 3-5 critical areas that need deep investigation
   - Prioritize based on industry and location

2. CRITICAL SUCCESS FACTORS:
   - What must go right for this startup to succeed?
   - Industry-specific success metrics

3. MAJOR RISKS AND CHALLENGES:
   - Market risks
   - Competition risks
   - Execution risks
   - Location-specific risks

4. DATA POINTS NEEDED:
   - Market size estimates
   - Customer acquisition channels
   - Pricing benchmarks
   - Cost structure benchmarks

5. AGENT GUIDANCE:
   - Specific instructions for market analyst
   - Specific instructions for competition analyst
   - Specific instructions for revenue strategist
   - Specific instructions for cost analyst

Provide a structured, actionable plan that will guide the specialized agents.""",
            idea=idea,
            industry=extracted_industry,
            location=extracted_location,
            web_search="Yes" if search_decision["search_needed"] else "No",
            similar_context=similar_context if similar_context else "No similar ideas found.",
            market_trends_section=f"LATEST MARKET TRENDS:\n{market_trends}" if market_trends else ""
        )
        
        response = await self.llm.ainvoke(prompt)
        
        # Store all context for other agents
        context["market_trends"] = market_trends
        context["search_results"] = search_results
        context["structured_context"] = structured_context
        context["search_decision"] = search_decision
        
        # Override industry and target_market with extracted values for consistency
        context["industry"] = extracted_industry
        context["target_market"] = extracted_location
        
        return response.content
