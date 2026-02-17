"""
Example usage of the AI Startup Feasibility Engine API
"""

import requests
import json


# API base URL
BASE_URL = "http://localhost:8000"


def analyze_startup_idea(idea: str, industry: str = None, target_market: str = None):
    """
    Analyze a startup idea using the API
    
    Args:
        idea: The startup idea description
        industry: Optional industry sector
        target_market: Optional target market
    """
    url = f"{BASE_URL}/analyze"
    
    payload = {
        "idea": idea,
        "industry": industry,
        "target_market": target_market
    }
    
    print(f"🚀 Analyzing startup idea...")
    print(f"Idea: {idea}\n")
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        
        print("=" * 80)
        print("FEASIBILITY REPORT")
        print("=" * 80)
        
        report = result["report"]
        
        print(f"\n📊 MARKET ANALYSIS")
        print("-" * 80)
        print(report["market_analysis"])
        
        print(f"\n👥 TARGET AUDIENCE")
        print("-" * 80)
        print(report["target_audience"])
        
        print(f"\n💰 REVENUE MODEL")
        print("-" * 80)
        print(report["revenue_model"])
        
        print(f"\n🏆 COMPETITION ANALYSIS")
        print("-" * 80)
        print(report["competition_analysis"])
        
        print(f"\n💸 COST STRUCTURE")
        print("-" * 80)
        print(report["cost_structure"])
        
        print(f"\n🚀 GO-TO-MARKET STRATEGY")
        print("-" * 80)
        print(report["go_to_market"])
        
        print(f"\n🎯 SUCCESS METRICS")
        print("-" * 80)
        print(f"Success Probability: {report['success_probability']}%")
        print(f"Best Location: {report['best_location']}")
        
        print(f"\n🔍 SIMILAR IDEAS ({len(result['similar_ideas'])})")
        print("-" * 80)
        for idx, similar in enumerate(result["similar_ideas"], 1):
            print(f"{idx}. {similar}")
        
        print(f"\n📚 SOURCES USED ({len(result['sources_used'])})")
        print("-" * 80)
        for idx, source in enumerate(result["sources_used"], 1):
            print(f"{idx}. {source}")
        
        print(f"\n🔎 CRITIQUE")
        print("-" * 80)
        print(result["critique"])
        
        print("\n" + "=" * 80)
        
        # Save to file
        filename = f"report_{idea[:30].replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"✅ Report saved to {filename}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None


def check_health():
    """Check API health"""
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        health = response.json()
        print("🏥 Health Check:")
        print(f"  Status: {health['status']}")
        print(f"  Version: {health['version']}")
        print(f"  Database: {'✅ Connected' if health['database_connected'] else '❌ Disconnected'}")
        
        return health
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return None


if __name__ == "__main__":
    # Check health first
    print("Checking API health...\n")
    check_health()
    print("\n" + "=" * 80 + "\n")
    
    # Example 1: SaaS startup
    analyze_startup_idea(
        idea="A SaaS platform that uses AI to automatically generate and optimize social media content for small businesses",
        industry="marketing tech",
        target_market="North America"
    )
    
    print("\n\n" + "=" * 80)
    print("=" * 80)
    print("\n")
    
    # Example 2: E-commerce startup
    # Uncomment to run
    # analyze_startup_idea(
    #     idea="An e-commerce marketplace for sustainable and eco-friendly products with carbon footprint tracking",
    #     industry="e-commerce",
    #     target_market="Europe"
    # )
