import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self) -> ChatGroq:
        """Initialize the Groq LLM"""
        api_key = os.getenv("GROQ_API_KEY")
        model = os.getenv("LLM_MODEL", "llama3-70b-8192")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        
        if not api_key:
            raise ValueError("GROQ_API_KEY must be set in environment variables")
        
        return ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=temperature
        )
    
    async def execute(self, context: Dict[str, Any]) -> str:
        """Execute the agent's task - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def _build_prompt(self, template: str, **kwargs) -> str:
        """Build a prompt from template and variables"""
        return template.format(**kwargs)
