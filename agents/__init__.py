"""Agents package for multi-agent architecture."""

from importlib import import_module

__all__ = [
    "BaseAgent",
    "PlannerAgent",
    "MarketIntelligenceAgent",
    "FinancialStrategyAgent",
    "GTMAgent",
    "SuccessProbabilityAgent",
    "CriticAgent",
]

_MODULE_MAP = {
    "BaseAgent": "agents.base_agent",
    "PlannerAgent": "agents.planner_agent",
    "MarketIntelligenceAgent": "agents.market_intelligence",
    "FinancialStrategyAgent": "agents.financial_strategy",
    "GTMAgent": "agents.strategy_agents",
    "SuccessProbabilityAgent": "agents.evaluation_agents",
    "CriticAgent": "agents.evaluation_agents",
}


def __getattr__(name: str):
    if name not in _MODULE_MAP:
        raise AttributeError(f"module 'agents' has no attribute '{name}'")
    module = import_module(_MODULE_MAP[name])
    return getattr(module, name)
