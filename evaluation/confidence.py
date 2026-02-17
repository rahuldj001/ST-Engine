"""
Confidence scoring for agent responses
"""
from typing import Dict, Any
import re


class ConfidenceScorer:
    """
    Calculate confidence scores for agent responses based on various factors
    """
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Estimate token count for text
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count (rough approximation: 1 token ≈ 4 characters)
        """
        # Rough estimation: 1 token ≈ 4 characters for English text
        return len(text) // 4
    
    @staticmethod
    def calculate_response_confidence(
        response: str,
        context_available: bool = True,
        search_data_available: bool = True,
        similar_ideas_count: int = 0
    ) -> float:
        """
        Calculate confidence score for an agent response
        
        Args:
            response: Agent response text
            context_available: Whether context was available
            search_data_available: Whether web search data was available
            similar_ideas_count: Number of similar ideas found
            
        Returns:
            Confidence score (0-1)
        """
        confidence = 0.5  # Base confidence
        
        # Factor 1: Response length (longer = more detailed = higher confidence)
        response_length = len(response)
        if response_length > 1000:
            confidence += 0.15
        elif response_length > 500:
            confidence += 0.10
        elif response_length > 200:
            confidence += 0.05
        else:
            confidence -= 0.10  # Very short responses are less confident
        
        # Factor 2: Presence of specific data points (numbers, percentages, etc.)
        data_points = len(re.findall(r'\d+%|\$\d+|\d+[KMB]|\d+,\d+', response))
        if data_points >= 5:
            confidence += 0.10
        elif data_points >= 3:
            confidence += 0.05
        
        # Factor 3: Context availability
        if context_available:
            confidence += 0.10
        else:
            confidence -= 0.15
        
        # Factor 4: Web search data availability
        if search_data_available:
            confidence += 0.10
        else:
            confidence -= 0.10
        
        # Factor 5: Similar ideas found (RAG context)
        if similar_ideas_count >= 3:
            confidence += 0.10
        elif similar_ideas_count >= 1:
            confidence += 0.05
        else:
            confidence -= 0.05
        
        # Factor 6: Presence of uncertainty markers
        uncertainty_markers = [
            'might', 'could', 'possibly', 'perhaps', 'maybe', 
            'uncertain', 'unclear', 'estimated', 'approximately',
            'roughly', 'around', 'about'
        ]
        uncertainty_count = sum(
            response.lower().count(marker) 
            for marker in uncertainty_markers
        )
        if uncertainty_count > 5:
            confidence -= 0.10
        elif uncertainty_count > 3:
            confidence -= 0.05
        
        # Factor 7: Presence of confidence markers
        confidence_markers = [
            'clearly', 'definitely', 'certainly', 'proven', 
            'established', 'confirmed', 'validated', 'verified'
        ]
        confidence_count = sum(
            response.lower().count(marker) 
            for marker in confidence_markers
        )
        if confidence_count >= 3:
            confidence += 0.05
        
        # Factor 8: Structured format (lists, sections)
        has_structure = bool(
            re.search(r'\n\s*[-*•]\s+', response) or  # Bullet points
            re.search(r'\n\s*\d+\.\s+', response)     # Numbered lists
        )
        if has_structure:
            confidence += 0.05
        
        # Clamp to [0, 1]
        return max(0.0, min(1.0, confidence))
    
    @staticmethod
    def calculate_planner_confidence(
        plan: str,
        industry_extracted: bool,
        location_extracted: bool,
        search_performed: bool,
        search_results_count: int
    ) -> float:
        """
        Calculate confidence for planner agent
        
        Args:
            plan: Planner response
            industry_extracted: Whether industry was extracted
            location_extracted: Whether location was extracted
            search_performed: Whether web search was performed
            search_results_count: Number of search results found
            
        Returns:
            Confidence score (0-1)
        """
        base_confidence = ConfidenceScorer.calculate_response_confidence(
            plan,
            context_available=True,
            search_data_available=search_performed and search_results_count > 0
        )
        
        # Bonus for successful extraction
        if industry_extracted:
            base_confidence += 0.05
        if location_extracted:
            base_confidence += 0.05
        
        # Bonus for search results
        if search_performed and search_results_count >= 2:
            base_confidence += 0.05
        
        return min(1.0, base_confidence)
    
    @staticmethod
    def calculate_analysis_confidence(
        analysis: str,
        plan_available: bool,
        market_trends_available: bool,
        similar_ideas_count: int
    ) -> float:
        """
        Calculate confidence for analysis agents (market, competition, revenue, etc.)
        
        Args:
            analysis: Agent analysis response
            plan_available: Whether planner output was available
            market_trends_available: Whether market trends were available
            similar_ideas_count: Number of similar ideas
            
        Returns:
            Confidence score (0-1)
        """
        return ConfidenceScorer.calculate_response_confidence(
            analysis,
            context_available=plan_available,
            search_data_available=market_trends_available,
            similar_ideas_count=similar_ideas_count
        )
    
    @staticmethod
    def calculate_critic_confidence(
        critique: str,
        revenue_issues_found: bool,
        competition_issues_found: bool,
        adjustment_made: bool
    ) -> float:
        """
        Calculate confidence for critic agent
        
        Args:
            critique: Critic response
            revenue_issues_found: Whether revenue issues were identified
            competition_issues_found: Whether competition issues were identified
            adjustment_made: Whether probability adjustment was made
            
        Returns:
            Confidence score (0-1)
        """
        base_confidence = ConfidenceScorer.calculate_response_confidence(
            critique,
            context_available=True,
            search_data_available=True
        )
        
        # Bonus for thorough analysis
        if revenue_issues_found or competition_issues_found:
            base_confidence += 0.05
        
        # Bonus for making adjustments (shows critical thinking)
        if adjustment_made:
            base_confidence += 0.05
        
        return min(1.0, base_confidence)
