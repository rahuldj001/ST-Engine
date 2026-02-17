from typing import Dict, Any
from agents.base_agent import BaseAgent


class SuccessProbabilityAgent(BaseAgent):
    """Agent that calculates success probability"""
    
    def __init__(self):
        super().__init__(
            name="Success Probability Analyst",
            role="Risk assessment and success probability expert"
        )
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate success probability and recommend best location
        
        Args:
            context: Complete analysis context
            
        Returns:
            Dictionary with success_probability (float) and best_location (str)
        """
        idea = context.get("idea", "")
        market_analysis = context.get("market_analysis", "")
        competition = context.get("competition_analysis", "")
        revenue_model = context.get("revenue_model", "")
        cost_structure = context.get("cost_structure", "")
        gtm_strategy = context.get("go_to_market", "")
        
        prompt = self._build_prompt(
            """You are a startup success probability expert and location strategist.

Startup Idea: {idea}

Market Analysis:
{market_analysis}

Competition:
{competition}

Revenue Model:
{revenue_model}

Cost Structure:
{cost_structure}

GTM Strategy:
{gtm_strategy}

Based on all the analysis, provide:

1. SUCCESS PROBABILITY SCORE (0-100):
Evaluate based on:
- Market opportunity and timing
- Competitive advantage
- Revenue model viability
- Cost efficiency
- GTM strategy strength
- Team requirements and execution complexity

Provide a single numerical score between 0 and 100.

2. BEST LOCATION:
Recommend the best city/region to launch this startup based on:
- Access to target customers
- Talent availability
- Ecosystem and funding
- Cost of operations
- Regulatory environment
- Market maturity

Format your response EXACTLY as:
SUCCESS_PROBABILITY: [number between 0-100]
BEST_LOCATION: [city/region name]
REASONING: [2-3 sentences explaining the score and location choice]""",
            idea=idea,
            market_analysis=market_analysis[:1000],
            competition=competition[:800],
            revenue_model=revenue_model[:800],
            cost_structure=cost_structure[:800],
            gtm_strategy=gtm_strategy[:800]
        )
        
        response = await self.llm.ainvoke(prompt)
        content = response.content
        
        # Parse the response
        success_probability = 50.0  # default
        best_location = "San Francisco, CA"  # default
        
        try:
            lines = content.split('\n')
            for line in lines:
                if line.startswith("SUCCESS_PROBABILITY:"):
                    prob_str = line.split(":", 1)[1].strip()
                    success_probability = float(prob_str)
                elif line.startswith("BEST_LOCATION:"):
                    best_location = line.split(":", 1)[1].strip()
        except Exception as e:
            print(f"Error parsing success probability response: {e}")
        
        return {
            "success_probability": success_probability,
            "best_location": best_location,
            "reasoning": content
        }


class CriticAgent(BaseAgent):
    """Enhanced critic agent that reviews, identifies issues, and adjusts success probability"""
    
    def __init__(self):
        super().__init__(
            name="Critic",
            role="Critical reviewer and quality assurance expert"
        )
    
    async def _analyze_revenue_assumptions(self, revenue_model: str, market_analysis: str) -> Dict[str, Any]:
        """
        Identify unrealistic revenue assumptions
        
        Args:
            revenue_model: Revenue model analysis
            market_analysis: Market analysis
            
        Returns:
            Dictionary with issues found and severity
        """
        prompt = f"""You are a revenue model expert. Analyze this revenue model for unrealistic assumptions.

Revenue Model:
{revenue_model[:1500]}

Market Context:
{market_analysis[:1000]}

Identify UNREALISTIC ASSUMPTIONS in these categories:

1. PRICING ASSUMPTIONS:
   - Is the pricing too optimistic?
   - Are conversion rates realistic?
   - Is willingness to pay validated?

2. GROWTH ASSUMPTIONS:
   - Are growth rates achievable?
   - Is customer acquisition timeline realistic?
   - Are scaling assumptions justified?

3. MARKET SIZE ASSUMPTIONS:
   - Is TAM/SAM/SOM realistic?
   - Are market penetration rates achievable?

Respond in this EXACT format:
UNREALISTIC_ASSUMPTIONS: [YES/NO]
SEVERITY: [LOW/MEDIUM/HIGH/CRITICAL]
ISSUES: [comma-separated list of specific issues, or "NONE"]
ADJUSTMENT_NEEDED: [percentage points to reduce success probability, 0-30]
REASONING: [2-3 sentences explaining the issues]"""

        response = await self.llm.ainvoke(prompt)
        content = response.content
        
        has_issues = False
        severity = "LOW"
        issues = []
        adjustment = 0
        reasoning = ""
        
        try:
            lines = content.split('\n')
            for line in lines:
                if line.startswith("UNREALISTIC_ASSUMPTIONS:"):
                    has_issues = "YES" in line.upper()
                elif line.startswith("SEVERITY:"):
                    severity = line.split(":", 1)[1].strip().upper()
                elif line.startswith("ISSUES:"):
                    issues_str = line.split(":", 1)[1].strip()
                    if issues_str != "NONE":
                        issues = [i.strip() for i in issues_str.split(",")]
                elif line.startswith("ADJUSTMENT_NEEDED:"):
                    adj_str = line.split(":", 1)[1].strip()
                    try:
                        adjustment = int(adj_str)
                    except:
                        adjustment = 0
                elif line.startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()
        except Exception as e:
            print(f"Error parsing revenue analysis: {e}")
        
        return {
            "has_issues": has_issues,
            "severity": severity,
            "issues": issues,
            "adjustment": adjustment,
            "reasoning": reasoning
        }
    
    async def _analyze_competition_intensity(self, competition_analysis: str, market_analysis: str) -> Dict[str, Any]:
        """
        Flag high competition markets
        
        Args:
            competition_analysis: Competition analysis
            market_analysis: Market analysis
            
        Returns:
            Dictionary with competition assessment
        """
        prompt = f"""You are a competitive intelligence expert. Assess the competition intensity.

Competition Analysis:
{competition_analysis[:1500]}

Market Analysis:
{market_analysis[:1000]}

Assess competition intensity based on:

1. NUMBER OF COMPETITORS:
   - How many direct competitors exist?
   - Are there dominant players?

2. MARKET SATURATION:
   - Is the market crowded?
   - Are there clear market leaders?

3. BARRIERS TO ENTRY:
   - How easy is it for new entrants?
   - What competitive advantages exist?

4. DIFFERENTIATION:
   - Is the value proposition unique?
   - Can competitors easily replicate?

Respond in this EXACT format:
COMPETITION_LEVEL: [LOW/MEDIUM/HIGH/EXTREME]
MARKET_SATURATION: [LOW/MEDIUM/HIGH]
DIFFERENTIATION_STRENGTH: [WEAK/MODERATE/STRONG]
RED_FLAGS: [comma-separated list of major concerns, or "NONE"]
ADJUSTMENT_NEEDED: [percentage points to reduce success probability, 0-25]
REASONING: [2-3 sentences explaining the assessment]"""

        response = await self.llm.ainvoke(prompt)
        content = response.content
        
        competition_level = "MEDIUM"
        saturation = "MEDIUM"
        differentiation = "MODERATE"
        red_flags = []
        adjustment = 0
        reasoning = ""
        
        try:
            lines = content.split('\n')
            for line in lines:
                if line.startswith("COMPETITION_LEVEL:"):
                    competition_level = line.split(":", 1)[1].strip().upper()
                elif line.startswith("MARKET_SATURATION:"):
                    saturation = line.split(":", 1)[1].strip().upper()
                elif line.startswith("DIFFERENTIATION_STRENGTH:"):
                    differentiation = line.split(":", 1)[1].strip().upper()
                elif line.startswith("RED_FLAGS:"):
                    flags_str = line.split(":", 1)[1].strip()
                    if flags_str != "NONE":
                        red_flags = [f.strip() for f in flags_str.split(",")]
                elif line.startswith("ADJUSTMENT_NEEDED:"):
                    adj_str = line.split(":", 1)[1].strip()
                    try:
                        adjustment = int(adj_str)
                    except:
                        adjustment = 0
                elif line.startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()
        except Exception as e:
            print(f"Error parsing competition analysis: {e}")
        
        return {
            "competition_level": competition_level,
            "saturation": saturation,
            "differentiation": differentiation,
            "red_flags": red_flags,
            "adjustment": adjustment,
            "reasoning": reasoning
        }
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """
        Review the complete feasibility report, identify issues, and adjust success probability
        
        Args:
            context: Complete analysis with all sections
            
        Returns:
            Critique with adjustments and detailed reasoning
        """
        idea = context.get("idea", "")
        report = context.get("full_report", {})
        original_probability = report.get("success_probability", 50.0)
        
        # Step 1: Analyze revenue assumptions
        print("  Analyzing revenue assumptions...")
        revenue_analysis = await self._analyze_revenue_assumptions(
            report.get("revenue_model", ""),
            report.get("market_analysis", "")
        )
        
        # Step 2: Analyze competition intensity
        print("  Analyzing competition intensity...")
        competition_analysis = await self._analyze_competition_intensity(
            report.get("competition_analysis", ""),
            report.get("market_analysis", "")
        )
        
        # Step 3: Calculate total adjustment
        total_adjustment = revenue_analysis["adjustment"] + competition_analysis["adjustment"]
        adjusted_probability = max(0, min(100, original_probability - total_adjustment))
        
        # Update context with adjusted probability
        context["adjusted_success_probability"] = adjusted_probability
        context["probability_adjustment"] = total_adjustment
        
        print(f"  Success probability: {original_probability}% -> {adjusted_probability}% (adjusted by -{total_adjustment}%)")
        
        # Step 4: Generate comprehensive critique
        prompt = self._build_prompt(
            """You are a critical reviewer of startup feasibility reports with expertise in identifying flaws.

Startup Idea: {idea}

COMPLETE FEASIBILITY REPORT:

Market Analysis:
{market_analysis}

Target Audience:
{target_audience}

Revenue Model:
{revenue_model}

Competition Analysis:
{competition_analysis}

Cost Structure:
{cost_structure}

Go-to-Market Strategy:
{go_to_market}

Original Success Probability: {original_probability}%
Adjusted Success Probability: {adjusted_probability}%
Adjustment: -{adjustment}%

CRITICAL FINDINGS:

Revenue Assumptions Analysis:
- Issues Found: {revenue_issues}
- Severity: {revenue_severity}
- Adjustment: -{revenue_adjustment}%
- Reasoning: {revenue_reasoning}

Competition Analysis:
- Competition Level: {competition_level}
- Market Saturation: {saturation}
- Differentiation: {differentiation}
- Red Flags: {red_flags}
- Adjustment: -{competition_adjustment}%
- Reasoning: {competition_reasoning}

Based on this analysis, provide a COMPREHENSIVE CRITIQUE covering:

1. UNREALISTIC REVENUE ASSUMPTIONS:
   - Specific assumptions that are too optimistic
   - Why they are unrealistic
   - What realistic assumptions should be

2. HIGH COMPETITION CONCERNS:
   - Major competitive threats
   - Market saturation issues
   - Differentiation weaknesses

3. WEAK ASSUMPTIONS (Other):
   - Questionable assumptions in other areas
   - Need for validation

4. MISSING INFORMATION:
   - Critical gaps in the analysis
   - Data needed for validation

5. LOGICAL GAPS:
   - Inconsistencies between sections
   - Logical flaws in reasoning

6. RISK FACTORS:
   - Underestimated risks
   - Major risks not mentioned

7. IMPROVEMENTS:
   - Specific recommendations for each section
   - Actionable next steps

8. ADJUSTED SUCCESS ASSESSMENT:
   - Why the probability was adjusted
   - What would need to change to improve it
   - Overall viability assessment

Be constructive but brutally honest. Focus on actionable insights.""",
            idea=idea,
            market_analysis=report.get("market_analysis", "N/A")[:1000],
            target_audience=report.get("target_audience", "N/A")[:800],
            revenue_model=report.get("revenue_model", "N/A")[:800],
            competition_analysis=report.get("competition_analysis", "N/A")[:800],
            cost_structure=report.get("cost_structure", "N/A")[:800],
            go_to_market=report.get("go_to_market", "N/A")[:800],
            original_probability=original_probability,
            adjusted_probability=adjusted_probability,
            adjustment=total_adjustment,
            revenue_issues=", ".join(revenue_analysis["issues"]) if revenue_analysis["issues"] else "None",
            revenue_severity=revenue_analysis["severity"],
            revenue_adjustment=revenue_analysis["adjustment"],
            revenue_reasoning=revenue_analysis["reasoning"],
            competition_level=competition_analysis["competition_level"],
            saturation=competition_analysis["saturation"],
            differentiation=competition_analysis["differentiation"],
            red_flags=", ".join(competition_analysis["red_flags"]) if competition_analysis["red_flags"] else "None",
            competition_adjustment=competition_analysis["adjustment"],
            competition_reasoning=competition_analysis["reasoning"]
        )
        
        response = await self.llm.ainvoke(prompt)
        
        # Build final critique with metadata
        critique_report = f"""CRITICAL REVIEW AND ADJUSTMENTS

ADJUSTED SUCCESS PROBABILITY: {adjusted_probability}% (Original: {original_probability}%, Adjustment: -{total_adjustment}%)

REVENUE ASSUMPTIONS REVIEW:
- Severity: {revenue_analysis['severity']}
- Issues: {', '.join(revenue_analysis['issues']) if revenue_analysis['issues'] else 'None identified'}
- Impact: -{revenue_analysis['adjustment']}% probability adjustment
- {revenue_analysis['reasoning']}

COMPETITION INTENSITY REVIEW:
- Competition Level: {competition_analysis['competition_level']}
- Market Saturation: {competition_analysis['saturation']}
- Differentiation Strength: {competition_analysis['differentiation']}
- Red Flags: {', '.join(competition_analysis['red_flags']) if competition_analysis['red_flags'] else 'None identified'}
- Impact: -{competition_analysis['adjustment']}% probability adjustment
- {competition_analysis['reasoning']}

DETAILED CRITIQUE:
{response.content}
"""
        
        return critique_report
