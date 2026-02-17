"""
Test script to verify the AI Startup Feasibility Engine
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import orchestrator


async def test_analysis():
    """Test the complete analysis workflow"""
    
    test_idea = "A mobile app that connects freelance graphic designers with small businesses for on-demand design work"
    
    print("=" * 80)
    print("Testing AI Startup Feasibility Engine")
    print("=" * 80)
    print(f"\nTest Idea: {test_idea}\n")
    print("=" * 80)
    
    try:
        # Run the analysis
        result = await orchestrator.analyze_startup_idea(
            idea=test_idea,
            industry="creative services",
            target_market="United States"
        )
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        
        print(f"\n📊 Market Analysis:")
        print(result.report.market_analysis[:300] + "...")
        
        print(f"\n👥 Target Audience:")
        print(result.report.target_audience[:300] + "...")
        
        print(f"\n💰 Revenue Model:")
        print(result.report.revenue_model[:300] + "...")
        
        print(f"\n🏆 Competition Analysis:")
        print(result.report.competition_analysis[:300] + "...")
        
        print(f"\n💸 Cost Structure:")
        print(result.report.cost_structure[:300] + "...")
        
        print(f"\n🚀 Go-to-Market Strategy:")
        print(result.report.go_to_market[:300] + "...")
        
        print(f"\n🎯 Success Probability: {result.report.success_probability}%")
        print(f"📍 Best Location: {result.report.best_location}")
        
        print(f"\n🔍 Similar Ideas Found: {len(result.similar_ideas)}")
        for idx, similar in enumerate(result.similar_ideas, 1):
            print(f"  {idx}. {similar}")
        
        print(f"\n📚 Sources Used: {len(result.sources_used)}")
        for idx, source in enumerate(result.sources_used, 1):
            print(f"  {idx}. {source}")
        
        print(f"\n🔎 Critique:")
        print(result.critique[:400] + "...")
        
        print("\n" + "=" * 80)
        print("✅ TEST PASSED")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_analysis())
