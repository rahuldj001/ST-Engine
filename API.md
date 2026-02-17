# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. For production use, implement API key authentication or OAuth2.

---

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns basic API information.

**Response:**
```json
{
  "message": "AI Startup Feasibility Engine API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. Health Check

**GET** `/health`

Check the health status of the API and database connection.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database_connected": true
}
```

**Status Values:**
- `healthy`: All systems operational
- `degraded`: Some systems not functioning properly

---

### 3. Analyze Startup Idea

**POST** `/analyze`

Generate a comprehensive feasibility report for a startup idea.

**Request Body:**
```json
{
  "idea": "string (required, min 10 characters)",
  "industry": "string (optional)",
  "target_market": "string (optional)"
}
```

**Example Request:**
```json
{
  "idea": "A mobile app that uses AI to help people find and book local fitness classes based on their preferences and schedule",
  "industry": "fitness tech",
  "target_market": "United States"
}
```

**Response:** `200 OK`
```json
{
  "idea": "string",
  "report": {
    "market_analysis": "string",
    "target_audience": "string",
    "revenue_model": "string",
    "competition_analysis": "string",
    "cost_structure": "string",
    "go_to_market": "string",
    "success_probability": 0-100,
    "best_location": "string"
  },
  "similar_ideas": ["string"],
  "sources_used": ["string"],
  "critique": "string"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `idea` | string | The original startup idea |
| `report.market_analysis` | string | Comprehensive market analysis including size, trends, and opportunities |
| `report.target_audience` | string | Detailed target audience identification and segmentation |
| `report.revenue_model` | string | Proposed revenue model and monetization strategy |
| `report.competition_analysis` | string | Analysis of competitors and market positioning |
| `report.cost_structure` | string | Expected cost structure and burn rate |
| `report.go_to_market` | string | Go-to-market strategy and channels |
| `report.success_probability` | number | Success probability score (0-100) |
| `report.best_location` | string | Recommended location for the startup |
| `similar_ideas` | array | List of similar ideas found in the database |
| `sources_used` | array | Web search queries used for market research |
| `critique` | string | Critical review and improvement suggestions |

**Error Responses:**

`422 Unprocessable Entity` - Invalid request body
```json
{
  "detail": [
    {
      "loc": ["body", "idea"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

`500 Internal Server Error` - Analysis failed
```json
{
  "detail": "Analysis failed: [error message]"
}
```

**Processing Time:** 
- Typical: 60-120 seconds
- Depends on: LLM response time, web search results, database queries

---

### 4. Get Similar Ideas

**GET** `/similar/{idea_id}?top_k=5`

Retrieve a stored idea and find similar ideas from the database.

**Path Parameters:**
- `idea_id` (integer, required): ID of the stored idea

**Query Parameters:**
- `top_k` (integer, optional, default=5): Number of similar ideas to retrieve

**Example Request:**
```
GET /similar/123?top_k=3
```

**Response:** `200 OK`
```json
{
  "idea": {
    "id": 123,
    "idea": "string",
    "report": {...},
    "created_at": "2026-02-13T20:00:00"
  },
  "similar_ideas": [
    {
      "id": 124,
      "idea": "string",
      "report": {...},
      "similarity": 0.85
    }
  ]
}
```

**Error Responses:**

`404 Not Found` - Idea not found
```json
{
  "detail": "Idea with ID 123 not found"
}
```

`500 Internal Server Error` - Retrieval failed
```json
{
  "detail": "Failed to retrieve similar ideas: [error message]"
}
```

---

## Usage Examples

### cURL

```bash
# Analyze a startup idea
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "AI-powered personal finance assistant for millennials",
    "industry": "fintech",
    "target_market": "United States"
  }'

# Health check
curl "http://localhost:8000/health"

# Get similar ideas
curl "http://localhost:8000/similar/1?top_k=5"
```

### Python (requests)

```python
import requests

# Analyze startup idea
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "idea": "AI-powered personal finance assistant for millennials",
        "industry": "fintech",
        "target_market": "United States"
    }
)
result = response.json()
print(f"Success Probability: {result['report']['success_probability']}%")

# Health check
health = requests.get("http://localhost:8000/health").json()
print(f"Status: {health['status']}")
```

### JavaScript (fetch)

```javascript
// Analyze startup idea
const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    idea: 'AI-powered personal finance assistant for millennials',
    industry: 'fintech',
    target_market: 'United States'
  })
});

const result = await response.json();
console.log(`Success Probability: ${result.report.success_probability}%`);
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing:
- Rate limiting per IP address
- API key-based quotas
- Request queuing for long-running analyses

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Explore all endpoints
- Test API calls directly in the browser
- View request/response schemas
- Download OpenAPI specification

---

## Error Handling

All endpoints return appropriate HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 422 | Validation Error (invalid request) |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

Error responses include a `detail` field with specific error information.

---

## Best Practices

1. **Timeout Handling**: Set appropriate timeouts (120-300 seconds) for the `/analyze` endpoint
2. **Retry Logic**: Implement exponential backoff for failed requests
3. **Caching**: Cache results for identical ideas to reduce processing time
4. **Async Processing**: For production, consider implementing async job processing with webhooks
5. **Validation**: Always validate input before sending to the API

---

## Webhooks (Future Feature)

Future versions may support webhooks for long-running analyses:

```json
POST /analyze
{
  "idea": "...",
  "webhook_url": "https://your-app.com/webhook"
}
```

The analysis would run asynchronously and POST results to your webhook URL when complete.

---

## OpenAPI Specification

Download the OpenAPI specification:
```
GET /openapi.json
```

This can be used to generate client libraries in various programming languages.

---

## Support

For API issues or questions:
- Check the interactive documentation at `/docs`
- Review error messages in the response
- Check application logs for detailed error information
- Ensure all environment variables are properly configured
