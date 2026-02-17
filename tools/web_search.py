from typing import List, Dict
from langchain_community.tools import DuckDuckGoSearchRun
from rag.embeddings import embedding_service


class WebSearchTool:
    """Web search tool using DuckDuckGo for live market trends"""
    
    def __init__(self):
        self.search = DuckDuckGoSearchRun()
    
    def search_market_trends(self, query: str, max_results: int = 5) -> str:
        """
        Search for market trends and information
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Formatted search results
        """
        try:
            results = self.search.run(query)
            return results
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    def search_and_embed(self, query: str) -> Dict[str, any]:
        """
        Search for information and generate embeddings
        
        Args:
            query: Search query
            
        Returns:
            Dictionary with search results and embeddings
        """
        # Perform search
        search_results = self.search_market_trends(query)
        
        # Generate embedding for the search results
        if search_results and not search_results.startswith("Search failed"):
            embedding = embedding_service.encode(search_results)
            return {
                "query": query,
                "results": search_results,
                "embedding": embedding
            }
        
        return {
            "query": query,
            "results": search_results,
            "embedding": None
        }
    
    def multi_search(self, queries: List[str]) -> List[Dict[str, any]]:
        """
        Perform multiple searches
        
        Args:
            queries: List of search queries
            
        Returns:
            List of search results with embeddings
        """
        results = []
        for query in queries:
            result = self.search_and_embed(query)
            results.append(result)
        
        return results


# Global instance
web_search_tool = WebSearchTool()
