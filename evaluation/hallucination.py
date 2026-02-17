"""
Hallucination risk detection
"""
from typing import Dict, List, Any, Tuple


class HallucinationDetector:
    """
    Detect potential hallucination risks in agent responses
    """
    
    @staticmethod
    def assess_data_grounding(
        search_performed: bool,
        search_results_count: int,
        similar_ideas_count: int,
        top_similarity_score: float
    ) -> Tuple[str, List[str]]:
        """
        Assess whether the analysis is grounded in real data
        
        Args:
            search_performed: Whether web search was performed
            search_results_count: Number of search results found
            similar_ideas_count: Number of similar ideas in database
            top_similarity_score: Highest similarity score
            
        Returns:
            Tuple of (risk_level, list_of_flags)
        """
        flags = []
        risk_score = 0
        
        # Check web search grounding
        if not search_performed:
            flags.append("⚠️ No web search performed - analysis may lack current market data")
            risk_score += 2
        elif search_results_count == 0:
            flags.append("🚨 Web search returned no results - high risk of hallucination")
            risk_score += 3
        elif search_results_count < 2:
            flags.append("⚠️ Limited web search results - analysis may be speculative")
            risk_score += 1
        
        # Check RAG grounding
        if similar_ideas_count == 0:
            flags.append("⚠️ No similar ideas in database - no historical context available")
            risk_score += 2
        elif top_similarity_score < 0.2:
            flags.append(f"⚠️ Very low similarity to existing ideas (max: {top_similarity_score:.1%}) - limited relevant context")
            risk_score += 2
        elif top_similarity_score < 0.4:
            flags.append(f"⚠️ Low similarity to existing ideas (max: {top_similarity_score:.1%}) - context may not be highly relevant")
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 5:
            risk_level = "CRITICAL"
        elif risk_score >= 3:
            risk_level = "HIGH"
        elif risk_score >= 1:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return risk_level, flags
    
    @staticmethod
    def check_response_consistency(
        market_analysis: str,
        competition_analysis: str,
        revenue_model: str
    ) -> List[str]:
        """
        Check for inconsistencies between different analyses
        
        Args:
            market_analysis: Market analysis text
            competition_analysis: Competition analysis text
            revenue_model: Revenue model text
            
        Returns:
            List of consistency warnings
        """
        warnings = []
        
        # Check if market analysis mentions "small market" but revenue is very optimistic
        market_lower = market_analysis.lower()
        revenue_lower = revenue_model.lower()
        
        small_market_indicators = ['small market', 'niche market', 'limited market', 'narrow market']
        high_revenue_indicators = ['billion', 'millions of users', 'rapid growth', 'exponential']
        
        has_small_market = any(indicator in market_lower for indicator in small_market_indicators)
        has_high_revenue = any(indicator in revenue_lower for indicator in high_revenue_indicators)
        
        if has_small_market and has_high_revenue:
            warnings.append("⚠️ Inconsistency: Small market size but high revenue projections")
        
        # Check if high competition but easy market entry mentioned
        competition_lower = competition_analysis.lower()
        
        high_competition_indicators = ['high competition', 'many competitors', 'saturated market', 'crowded market']
        easy_entry_indicators = ['low barriers', 'easy to enter', 'simple to start']
        
        has_high_competition = any(indicator in competition_lower for indicator in high_competition_indicators)
        has_easy_entry = any(indicator in market_lower or indicator in revenue_lower for indicator in easy_entry_indicators)
        
        if has_high_competition and has_easy_entry:
            warnings.append("⚠️ Inconsistency: High competition but low barriers to entry mentioned")
        
        return warnings
    
    @staticmethod
    def detect_vague_claims(response: str) -> List[str]:
        """
        Detect vague or unsubstantiated claims
        
        Args:
            response: Agent response text
            
        Returns:
            List of vague claim warnings
        """
        warnings = []
        
        # Check for vague quantifiers without data
        vague_patterns = [
            ('many', 'users'),
            ('significant', 'growth'),
            ('large', 'market'),
            ('substantial', 'revenue'),
            ('considerable', 'opportunity'),
            ('numerous', 'customers')
        ]
        
        response_lower = response.lower()
        vague_count = 0
        
        for qualifier, noun in vague_patterns:
            pattern = f"{qualifier} {noun}"
            if pattern in response_lower:
                vague_count += 1
        
        if vague_count >= 3:
            warnings.append(f"⚠️ Multiple vague claims detected ({vague_count}) - lacks specific data points")
        
        # Check for specific numbers/data
        import re
        has_numbers = bool(re.search(r'\d+%|\$\d+|\d+[KMB]|\d+,\d+', response))
        
        if not has_numbers and len(response) > 500:
            warnings.append("⚠️ Long response with no specific numbers or data points")
        
        return warnings
    
    @staticmethod
    def generate_hallucination_report(
        search_performed: bool,
        search_results_count: int,
        similar_ideas_count: int,
        top_similarity_score: float,
        market_analysis: str = "",
        competition_analysis: str = "",
        revenue_model: str = ""
    ) -> Dict[str, Any]:
        """
        Generate comprehensive hallucination risk report
        
        Args:
            search_performed: Whether web search was performed
            search_results_count: Number of search results
            similar_ideas_count: Number of similar ideas
            top_similarity_score: Top similarity score
            market_analysis: Market analysis text (optional)
            competition_analysis: Competition analysis text (optional)
            revenue_model: Revenue model text (optional)
            
        Returns:
            Dictionary with risk assessment
        """
        # Assess data grounding
        risk_level, grounding_flags = HallucinationDetector.assess_data_grounding(
            search_performed,
            search_results_count,
            similar_ideas_count,
            top_similarity_score
        )
        
        # Check consistency
        consistency_warnings = []
        if market_analysis and competition_analysis and revenue_model:
            consistency_warnings = HallucinationDetector.check_response_consistency(
                market_analysis,
                competition_analysis,
                revenue_model
            )
        
        # Detect vague claims
        vague_warnings = []
        if market_analysis:
            vague_warnings.extend(HallucinationDetector.detect_vague_claims(market_analysis))
        
        # Combine all flags
        all_flags = grounding_flags + consistency_warnings + vague_warnings
        
        # Generate recommendations
        recommendations = []
        
        if risk_level in ["HIGH", "CRITICAL"]:
            recommendations.append("🔍 Manually verify all claims and data points")
            recommendations.append("📊 Seek additional data sources before making decisions")
        
        if not search_performed or search_results_count == 0:
            recommendations.append("🌐 Perform manual web research to validate findings")
        
        if similar_ideas_count == 0:
            recommendations.append("📚 Build up database with more similar ideas for better context")
        
        if consistency_warnings:
            recommendations.append("⚖️ Review and resolve inconsistencies between sections")
        
        if vague_warnings:
            recommendations.append("📈 Request specific data points and quantitative analysis")
        
        return {
            "risk_level": risk_level,
            "flags": all_flags,
            "recommendations": recommendations,
            "data_grounding": {
                "search_performed": search_performed,
                "search_results_count": search_results_count,
                "similar_ideas_count": similar_ideas_count,
                "top_similarity_score": round(top_similarity_score, 3)
            }
        }
    
    @staticmethod
    def print_hallucination_report(report: Dict[str, Any]):
        """Print formatted hallucination risk report"""
        print("\n" + "="*80)
        print("HALLUCINATION RISK ASSESSMENT")
        print("="*80)
        
        # Risk level with color coding
        risk_level = report["risk_level"]
        risk_emoji = {
            "LOW": "✅",
            "MEDIUM": "⚠️",
            "HIGH": "🚨",
            "CRITICAL": "🔴"
        }
        
        print(f"\n{risk_emoji.get(risk_level, '❓')} RISK LEVEL: {risk_level}")
        
        # Data grounding
        grounding = report["data_grounding"]
        print(f"\n📊 DATA GROUNDING:")
        print(f"  Web Search: {'✓' if grounding['search_performed'] else '✗'} ({grounding['search_results_count']} results)")
        print(f"  Similar Ideas: {grounding['similar_ideas_count']} found")
        print(f"  Top Similarity: {grounding['top_similarity_score']:.1%}")
        
        # Flags
        if report["flags"]:
            print(f"\n⚠️  RISK FLAGS ({len(report['flags'])}):")
            for flag in report["flags"]:
                print(f"  {flag}")
        else:
            print(f"\n✅ No risk flags detected")
        
        # Recommendations
        if report["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"  {rec}")
        
        print("\n" + "="*80 + "\n")
