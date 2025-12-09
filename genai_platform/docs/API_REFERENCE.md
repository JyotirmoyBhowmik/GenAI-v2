# GenAI Platform — REST API Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently uses division/department context (add Bearer token in production).

## Endpoints

### Health & Status

#### GET /health
Check system health status.

**Response:**
```json
{
  "status": "operational",
  "version": "1.0.0",
  "components": {
    "configuration": true,
    "models": true
  }
}
```

#### GET /version
Get version information.

### Query Processing

#### POST /query
Process a user query with AI.

**Request:**
```json
{
  "prompt": "Analyze sales trends for FMCG",
  "division_id": "fmcg",
  "department_id": "fmcg_sales",
  "persona_id": "sales_coach",
  "model_id": "gpt-4"
}
```

**Response:**
```json
{
  "text": "Based on the data...",
  "model_id": "gpt-4",
  "provider": "openai",
  "tokens_used": 250,
  "cost": 0.015,
  "redacted_pii": []
}
```

### Configuration

#### GET /config
Get current configuration.

**Response:**
```json
{
  "divisions": [...],
  "models": [...],
  "personas": [...]
}
```

#### GET /divisions
List all divisions.

#### GET /divisions/{division_id}
Get specific division.

#### GET /models
List all available models.

#### GET /models/{model_id}
Get model details.

#### GET /personas
List all personas.

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |

## Examples

### Query Example
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are top products by revenue?",
    "division_id": "fmcg",
    "department_id": "fmcg_sales",
    "persona_id": "sales_coach"
  }'
```

### Get Configuration
```bash
curl http://localhost:8000/api/config
```

### Check Health
```bash
curl http://localhost:8000/api/health
```

---
**Version**: 1.0.0
**Last Updated**: December 2024
