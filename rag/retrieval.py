import os
from typing import List, Dict
from database.vector_db import vector_db
from rag.embeddings import embedding_service
from dotenv import load_dotenv

load_dotenv()


class RAGService:
    """Retrieval-Augmented Generation service for startup ideas"""
    
    def __init__(self):
        self.top_k = int(os.getenv("TOP_K_SIMILAR", "5"))
    
    async def retrieve_similar_ideas(self, idea: str) -> List[Dict]:
        """
        Retrieve similar startup ideas from the vector database
        
        Args:
            idea: The startup idea to search for
            
        Returns:
            List of similar ideas with their reports and similarity scores
        """
        # Generate embedding for the input idea
        idea_embedding = embedding_service.encode(idea)
        
        # Search for similar ideas in the vector database
        similar_ideas = vector_db.search_similar_ideas(idea_embedding, self.top_k)
        
        return similar_ideas
    
    async def store_idea_with_report(self, idea: str, report: dict) -> int:
        """
        Store a startup idea with its feasibility report
        
        Args:
            idea: The startup idea
            report: The generated feasibility report
            
        Returns:
            ID of the stored idea
        """
        # Generate embedding for the idea
        idea_embedding = embedding_service.encode(idea)
        
        # Store in vector database
        idea_id = vector_db.insert_idea(idea, idea_embedding, report)
        
        return idea_id
    
    def build_context_from_similar_ideas(self, similar_ideas: List[Dict]) -> str:
        """
        Build context string from similar ideas for LLM prompt
        
        Args:
            similar_ideas: List of similar ideas with reports
            
        Returns:
            Formatted context string
        """
        if not similar_ideas:
            return "No similar ideas found in the database."
        
        context_parts = ["Here are similar startup ideas that have been analyzed previously:\n"]
        
        for idx, item in enumerate(similar_ideas, 1):
            similarity = item.get('similarity', 0)
            idea = item.get('idea', 'N/A')
            report = item.get('report', {})
            
            context_parts.append(f"\n{idx}. Similar Idea (Similarity: {similarity:.2%}):")
            context_parts.append(f"   Idea: {idea}")
            
            if report:
                context_parts.append(f"   Market Analysis: {report.get('market_analysis', 'N/A')[:200]}...")
                context_parts.append(f"   Success Probability: {report.get('success_probability', 'N/A')}%")
                context_parts.append(f"   Revenue Model: {report.get('revenue_model', 'N/A')[:150]}...")
        
        return "\n".join(context_parts)


# Global instance
rag_service = RAGService()
