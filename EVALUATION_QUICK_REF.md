# Evaluation Layer - Quick Reference

## 🎯 What It Does

The evaluation layer automatically tracks and assesses the quality of AI-generated startup feasibility reports.

---

## 📊 Key Metrics

### **1. Token Usage**
- Tracks tokens used by each agent
- Estimates total cost
- Helps optimize prompts

### **2. Confidence Scores (0-100%)**
- Per-agent confidence
- Overall weighted confidence
- Based on response quality, data availability, structure

### **3. Retrieval Similarity**
- Number of similar ideas found
- Similarity scores (0-100%)
- Indicates RAG effectiveness

### **4. Hallucination Risk**
- **LOW**: Well-grounded ✅
- **MEDIUM**: Some gaps ⚠️
- **HIGH**: Verify manually 🚨
- **CRITICAL**: Don't trust 🔴

---

## 🚨 Hallucination Flags

### **When Raised:**
- ⚠️ No web search performed
- 🚨 Web search returned no results
- ⚠️ No similar ideas in database
- ⚠️ Low similarity to existing ideas
- ⚠️ Inconsistencies detected
- ⚠️ Vague claims without data

### **What To Do:**
1. Review flagged sections manually
2. Verify claims with external sources
3. Don't make decisions solely on flagged analysis
4. Consider re-running with more context

---

## 📈 Sample Output

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
    - ⚠️ Limited web search results
    - ⚠️ Low similarity to existing ideas (max: 38.2%)

🔍 RETRIEVAL METRICS:
  Similar Ideas Found: 3
  Top Similarity Score: 38.2%

🌐 WEB SEARCH METRICS:
  Search Performed: Yes
  Results Found: 1

🤖 AGENT METRICS:
  Planner: Tokens: 1,245 | Confidence: 82.0%
  Market Analyst: Tokens: 2,156 | Confidence: 85.0%
  ...

================================================================================
HALLUCINATION RISK ASSESSMENT
================================================================================

⚠️ RISK LEVEL: MEDIUM

💡 RECOMMENDATIONS:
  📊 Seek additional data sources before making decisions
  📚 Build up database with more similar ideas
```

---

## 🎯 Quick Interpretation

### **Confidence Scores**
- **90%+**: Trust it ✅
- **75-89%**: Generally reliable ✓
- **60-74%**: Review key sections ⚠️
- **< 60%**: Verify manually 🚨

### **Hallucination Risk**
- **LOW**: Proceed confidently ✅
- **MEDIUM**: Verify key claims ⚠️
- **HIGH**: Manual verification required 🚨
- **CRITICAL**: Do not use 🔴

### **Similarity Scores**
- **> 70%**: Very similar ideas exist
- **50-70%**: Related context available
- **30-50%**: Some relevant context
- **< 30%**: Limited context (higher risk)

---

## 🔧 Usage

### **Automatic (Default)**
```python
# Evaluation happens automatically
response = await orchestrator.analyze_startup_idea(
    idea="Your startup idea",
    industry="tech",
    target_market="US"
)

# Metrics printed to console
# Also available as:
print(response.evaluation_metrics)
print(response.hallucination_report)
```

### **Access Metrics**
```python
# Get evaluation summary
metrics = response.evaluation_metrics

print(f"Total Tokens: {metrics['total_tokens']}")
print(f"Confidence: {metrics['overall_confidence']}")
print(f"Risk: {metrics['hallucination_risk']}")
```

---

## ✅ Best Practices

### **1. Always Check Risk Level**
- MEDIUM or higher → Verify manually
- CRITICAL → Don't use without validation

### **2. Review Low Confidence Agents**
- Identify agents with < 60% confidence
- Review their outputs carefully
- Consider improving prompts

### **3. Monitor Token Usage**
- Track costs over time
- Optimize high-token agents
- Set budgets if needed

### **4. Build Up Database**
- Low similarity = higher risk
- Add more similar ideas to database
- Improves future analyses

---

## 🚨 Red Flags

### **Immediate Action Required:**
- ❌ Hallucination Risk: CRITICAL
- ❌ Overall Confidence < 50%
- ❌ No web search + No similar ideas
- ❌ Multiple consistency warnings

### **Review Recommended:**
- ⚠️ Hallucination Risk: HIGH
- ⚠️ Overall Confidence < 70%
- ⚠️ Low similarity scores (< 30%)
- ⚠️ Any hallucination flags

---

## 📝 Common Scenarios

### **Scenario 1: Novel Idea**
```
Similar Ideas: 0
Similarity: 0%
Risk: HIGH
→ Expected for truly novel ideas
→ Verify all claims manually
→ Add to database for future reference
```

### **Scenario 2: Well-Researched Market**
```
Similar Ideas: 5+
Similarity: 70%+
Search Results: 3+
Risk: LOW
→ High confidence in analysis
→ Good data grounding
```

### **Scenario 3: Emerging Technology**
```
Search Performed: Yes
Results: Limited
Risk: MEDIUM
→ Fast-moving market
→ Verify latest trends
→ Re-run periodically
```

---

## 📊 Files Created

```
evaluation/
├── __init__.py              # Package init
├── metrics.py               # Token & metrics tracking
├── confidence.py            # Confidence scoring
└── hallucination.py         # Hallucination detection
```

---

## 🎓 Learn More

See **EVALUATION_LAYER.md** for:
- Detailed scoring algorithms
- Advanced usage examples
- Customization options
- Debugging guides

---

**Remember:** The evaluation layer helps you **trust but verify**. Use it to identify when manual review is needed!
