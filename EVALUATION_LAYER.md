# Evaluation Layer Documentation

## Overview

The evaluation layer provides comprehensive tracking and assessment of the AI Startup Feasibility Engine's analysis quality, including token usage, confidence scoring, retrieval metrics, and hallucination risk detection.

---

## 🎯 Components

### 1. **Metrics Tracker** (`evaluation/metrics.py`)
Tracks comprehensive metrics throughout the analysis workflow.

### 2. **Confidence Scorer** (`evaluation/confidence.py`)
Calculates confidence scores for agent responses based on multiple factors.

### 3. **Hallucination Detector** (`evaluation/hallucination.py`)
Detects potential hallucination risks and data grounding issues.

---

## 📊 Metrics Tracked

### **Token Usage**
- **Per-Agent Tokens**: Estimated tokens used by each agent
- **Total Tokens**: Sum of all agent token usage
- **Estimation Method**: ~4 characters per token (rough approximation)

**Example:**
```
Total Tokens Used: 15,234
  Planner: 1,245 tokens
  Market Analyst: 2,156 tokens
  Competition Analyst: 1,987 tokens
  ...
```

### **Execution Time**
- **Per-Agent Time**: Milliseconds spent in each agent
- **Total Execution Time**: End-to-end analysis time
- **Retrieval Time**: Time spent on RAG retrieval
- **Search Time**: Time spent on web searches

**Example:**
```
Total Execution Time: 87.5s
  Planner: 8,234ms
  Market Analyst: 12,456ms
  ...
```

### **Confidence Scores**
- **Per-Agent Confidence**: 0-1 score for each agent's response
- **Overall Confidence**: Weighted average across all agents
- **Factors Considered**:
  - Response length and detail
  - Presence of specific data points
  - Context availability
  - Web search data availability
  - Similar ideas found
  - Uncertainty vs. confidence markers
  - Structured formatting

**Example:**
```
Overall Confidence: 78.5%
  Planner: 82%
  Market Analyst: 85%
  Competition Analyst: 76%
  ...
```

### **Retrieval Metrics**
- **Similar Ideas Count**: Number of similar ideas found
- **Top Similarity Score**: Highest similarity score
- **Average Similarity**: Mean similarity across results
- **Retrieval Time**: Time to retrieve from vector DB

**Example:**
```
Similar Ideas Found: 5
Top Similarity Score: 67.3%
Average Similarity: 45.2%
Retrieval Time: 234ms
```

### **Search Metrics**
- **Search Performed**: Boolean flag
- **Queries Count**: Number of search queries executed
- **Results Found**: Number of queries with results
- **Search Time**: Time spent searching

**Example:**
```
Search Performed: Yes
Queries Executed: 3
Results Found: 2
Search Time: 1,234ms
```

---

## 🎯 Confidence Scoring

### **Scoring Factors**

#### 1. **Response Length**
- Longer, more detailed responses → Higher confidence
- Very short responses → Lower confidence

#### 2. **Data Points**
- Presence of numbers, percentages, dollar amounts
- More specific data → Higher confidence

#### 3. **Context Availability**
- Plan available → +10%
- Market trends available → +10%
- Similar ideas found → +5-10%

#### 4. **Uncertainty Markers**
- Words like "might", "could", "possibly" → Lower confidence
- Many uncertainty markers → -5-10%

#### 5. **Confidence Markers**
- Words like "clearly", "definitely", "proven" → Higher confidence

#### 6. **Structured Format**
- Bullet points, numbered lists → +5%

### **Agent-Specific Scoring**

#### **Planner Confidence**
```python
Base confidence
+ Industry extracted: +5%
+ Location extracted: +5%
+ Search results found: +5%
```

#### **Analysis Agents Confidence**
```python
Base confidence
+ Plan available: +10%
+ Market trends available: +10%
+ Similar ideas (3+): +10%
```

#### **Critic Confidence**
```python
Base confidence
+ Issues identified: +5%
+ Adjustments made: +5%
```

---

## 🚨 Hallucination Risk Detection

### **Risk Levels**
- **LOW**: Well-grounded analysis with sufficient data
- **MEDIUM**: Some data gaps but generally reliable
- **HIGH**: Significant data gaps, verify manually
- **CRITICAL**: Severe lack of grounding, high hallucination risk

### **Risk Factors**

#### 1. **Web Search Grounding**
```
No search performed → +2 risk score
No search results → +3 risk score
Limited results (< 2) → +1 risk score
```

#### 2. **RAG Grounding**
```
No similar ideas → +2 risk score
Very low similarity (< 0.2) → +2 risk score
Low similarity (< 0.4) → +1 risk score
```

#### 3. **Consistency Checks**
- Small market + high revenue projections → Warning
- High competition + low barriers → Warning

#### 4. **Vague Claims**
- Multiple vague quantifiers without data → Warning
- Long responses with no numbers → Warning

### **Risk Score Mapping**
```
Score >= 5 → CRITICAL
Score >= 3 → HIGH
Score >= 1 → MEDIUM
Score = 0 → LOW
```

---

## 📋 Evaluation Report

### **Sample Output**

```
================================================================================
EVALUATION METRICS SUMMARY
================================================================================

📊 OVERALL METRICS:
  Total Tokens Used: 15,234
  Total Execution Time: 87.5s
  Overall Confidence: 78.5%
  Hallucination Risk: MEDIUM

⚠️  HALLUCINATION FLAGS:
    - ⚠️ Limited web search results - analysis may be speculative
    - ⚠️ Low similarity to existing ideas (max: 38.2%) - context may not be highly relevant

🔍 RETRIEVAL METRICS:
  Similar Ideas Found: 3
  Top Similarity Score: 38.2%
  Average Similarity: 25.7%
  Retrieval Time: 234ms

🌐 WEB SEARCH METRICS:
  Search Performed: Yes
  Queries Executed: 3
  Results Found: 1
  Search Time: 1,234ms

🤖 AGENT METRICS:
  Planner:
    Tokens: 1,245 | Time: 8,234ms | Confidence: 82.0%
  Market Analyst:
    Tokens: 2,156 | Time: 12,456ms | Confidence: 85.0%
  Competition Analyst:
    Tokens: 1,987 | Time: 11,234ms | Confidence: 76.0%
  ...

================================================================================

================================================================================
HALLUCINATION RISK ASSESSMENT
================================================================================

⚠️ RISK LEVEL: MEDIUM

📊 DATA GROUNDING:
  Web Search: ✓ (1 results)
  Similar Ideas: 3 found
  Top Similarity: 38.2%

⚠️  RISK FLAGS (2):
  ⚠️ Limited web search results - analysis may be speculative
  ⚠️ Low similarity to existing ideas (max: 38.2%) - context may not be highly relevant

💡 RECOMMENDATIONS:
  📊 Seek additional data sources before making decisions
  📚 Build up database with more similar ideas for better context

================================================================================
```

---

## 🔧 Usage

### **Automatic Tracking**

The evaluation layer is automatically integrated into the orchestrator. No additional code needed!

```python
from agents.orchestrator import orchestrator

# Analysis automatically includes evaluation
response = await orchestrator.analyze_startup_idea(
    idea="AI-powered meal planning app",
    industry="food tech",
    target_market="United States"
)

# Evaluation metrics are printed automatically
# Also available as attributes
print(response.evaluation_metrics)
print(response.hallucination_report)
```

### **Manual Tracking**

For custom workflows:

```python
from evaluation.metrics import evaluation_tracker
from evaluation.confidence import ConfidenceScorer
from evaluation.hallucination import HallucinationDetector

# Start tracking
evaluation_tracker.reset()
evaluation_tracker.start_tracking()

# Track agent execution
response = await agent.execute(context)
tokens = ConfidenceScorer.estimate_tokens(response)
confidence = ConfidenceScorer.calculate_response_confidence(response)
evaluation_tracker.add_agent_metrics("Agent Name", tokens, time_ms, confidence)

# Set retrieval metrics
evaluation_tracker.set_retrieval_metrics(similar_ideas, retrieval_time_ms)

# Set search metrics
evaluation_tracker.set_search_metrics(search_performed, queries, results, search_time_ms)

# Calculate overall confidence
overall_confidence = evaluation_tracker.calculate_overall_confidence()

# Assess hallucination risk
risk_level = evaluation_tracker.assess_hallucination_risk()

# End tracking
evaluation_tracker.end_tracking()

# Print summary
evaluation_tracker.print_summary()

# Get summary dict
summary = evaluation_tracker.get_summary()
```

---

## 📈 Interpretation Guide

### **Confidence Scores**

| Score | Interpretation | Action |
|-------|---------------|--------|
| 90-100% | Very High | Trust the analysis |
| 75-89% | High | Generally reliable |
| 60-74% | Medium | Review key sections |
| 40-59% | Low | Verify manually |
| 0-39% | Very Low | Do not rely on analysis |

### **Hallucination Risk**

| Risk | Interpretation | Action |
|------|---------------|--------|
| LOW | Well-grounded | Proceed with confidence |
| MEDIUM | Some gaps | Verify key claims |
| HIGH | Significant gaps | Manual verification required |
| CRITICAL | Severe issues | Do not use without validation |

### **Token Usage**

| Tokens | Cost Estimate* | Notes |
|--------|---------------|-------|
| < 10K | ~$0.10 | Efficient |
| 10-20K | ~$0.20 | Normal |
| 20-50K | ~$0.50 | High usage |
| > 50K | > $1.00 | Very high, optimize |

*Approximate based on Groq pricing

### **Similarity Scores**

| Score | Interpretation |
|-------|---------------|
| > 70% | Very similar idea exists |
| 50-70% | Related ideas exist |
| 30-50% | Some relevant context |
| < 30% | Limited relevant context |

---

## 🎯 Best Practices

### **1. Monitor Confidence Scores**
- Review agents with confidence < 60%
- Investigate causes of low confidence
- Consider re-running with more context

### **2. Address Hallucination Flags**
- Always review CRITICAL risk analyses
- Verify claims when web search fails
- Build up similar ideas database

### **3. Optimize Token Usage**
- Monitor total token usage
- Identify high-token agents
- Optimize prompts if needed

### **4. Track Trends**
- Compare metrics across analyses
- Identify patterns in confidence/risk
- Improve system based on insights

---

## 🔍 Debugging Low Confidence

### **If Overall Confidence < 60%:**

1. **Check Retrieval Metrics**
   - Are similar ideas found?
   - Is similarity score high enough?
   - Action: Build up database

2. **Check Search Metrics**
   - Did web search succeed?
   - Were results found?
   - Action: Verify search tool works

3. **Check Agent Responses**
   - Are responses detailed enough?
   - Do they contain specific data?
   - Action: Improve prompts

4. **Check Context**
   - Is the idea too novel/unique?
   - Is the industry well-defined?
   - Action: Provide more context

---

## 🚨 Addressing High Hallucination Risk

### **If Risk = HIGH or CRITICAL:**

1. **Verify Data Grounding**
   - Manually search for market data
   - Validate key claims
   - Cross-reference with external sources

2. **Check Consistency**
   - Review for contradictions
   - Verify logic between sections
   - Resolve inconsistencies

3. **Seek Additional Data**
   - Perform manual research
   - Add similar ideas to database
   - Re-run analysis with more context

4. **Use with Caution**
   - Don't make decisions based solely on analysis
   - Treat as preliminary research
   - Validate all assumptions

---

## 📊 Metrics Export

### **Save to File**
```python
evaluation_tracker.save_to_file("metrics_report.json")
```

### **JSON Format**
```json
{
  "total_tokens": 15234,
  "total_execution_time_ms": 87500,
  "overall_confidence": 0.785,
  "hallucination_risk": "MEDIUM",
  "hallucination_flags": [...],
  "agent_metrics": [...],
  "retrieval_metrics": {...},
  "search_metrics": {...}
}
```

---

## 🎓 Advanced Usage

### **Custom Confidence Calculation**
```python
from evaluation.confidence import ConfidenceScorer

confidence = ConfidenceScorer.calculate_response_confidence(
    response=agent_response,
    context_available=True,
    search_data_available=True,
    similar_ideas_count=5
)
```

### **Custom Hallucination Report**
```python
from evaluation.hallucination import HallucinationDetector

report = HallucinationDetector.generate_hallucination_report(
    search_performed=True,
    search_results_count=2,
    similar_ideas_count=3,
    top_similarity_score=0.65,
    market_analysis=market_text,
    competition_analysis=competition_text,
    revenue_model=revenue_text
)

HallucinationDetector.print_hallucination_report(report)
```

---

## ✅ Summary

The evaluation layer provides:

✅ **Token Usage Tracking** - Monitor costs and optimize
✅ **Confidence Scoring** - Assess response quality
✅ **Retrieval Metrics** - Understand RAG effectiveness
✅ **Search Metrics** - Track web search success
✅ **Hallucination Detection** - Identify data grounding issues
✅ **Comprehensive Reports** - Detailed metrics and recommendations

**Use this layer to:**
- Ensure analysis quality
- Identify potential issues
- Optimize system performance
- Make informed decisions about trust level
