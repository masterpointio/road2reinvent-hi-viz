# AWS Bill Burner API - FastAPI Lambda

This Lambda function acts as a proxy between the frontend and the AgentCore backend, providing REST API endpoints for burn plan generation and roast commentary.

## Architecture

```
Frontend → API Gateway → FastAPI Lambda → AgentCore SDK → Strands Agent
```

## Endpoints

### Health Check
- **GET** `/api/health`
- Returns service status and AgentCore configuration status

### Generate Burn Plan
- **POST** `/api/burn-plan`
- Request body:
  ```json
  {
    "config": {
      "amount": "$1000",
      "timeline": 30,
      "stupidity": "Moderately stupid",
      "architecture": "serverless",
      "burning_style": "horizontal"
    }
  }
  ```
- Returns burn plan with session ID

### Generate Roast
- **POST** `/api/roast`
- Request body:
  ```json
  {
    "session_id": "uuid-here"
  }
  ```
- Returns roast commentary (not yet implemented - requires DynamoDB)

## Environment Variables

Required environment variables:

- `AGENTCORE_AGENT_RUNTIME_ARN`: ARN of the AgentCore agent runtime (e.g., `arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/agent_name-XXXXX`)
- `AWS_REGION`: AWS region (automatically set by Lambda)

## Project Structure

```
lib/lambda/fastapi/
├── app.py                      # FastAPI application
├── main.py                     # Lambda handler with Mangum
├── models.py                   # Pydantic models
├── requirements.txt            # Python dependencies
├── routers/
│   ├── burn_plan.py           # Burn plan endpoints
│   └── roast.py               # Roast endpoints
├── services/
│   └── strands_service.py     # Strands agent integration
└── utils/
    └── agentcore_client.py    # AgentCore SDK wrapper
```

## Local Development

1. Install dependencies:
   ```bash
   cd lib/lambda/fastapi
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export AGENTCORE_AGENT_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/agent_name-XXXXX"
   export AWS_REGION="us-east-1"
   ```

3. Run locally:
   ```bash
   uvicorn app:app --reload
   ```

## Deployment

The Lambda is deployed via CDK with IAM authentication for AgentCore:

```typescript
environment: {
  AGENTCORE_AGENT_RUNTIME_ARN: process.env.AGENTCORE_AGENT_RUNTIME_ARN || '',
  AWS_REGION: this.region,
}
```

The Lambda execution role is automatically granted permissions to invoke the AgentCore agent runtime:

```typescript
fastapiFunction.addToRolePolicy(
  new iam.PolicyStatement({
    effect: iam.Effect.ALLOW,
    actions: ['bedrock-agentcore:InvokeAgentRuntime'],
    resources: [process.env.AGENTCORE_AGENT_RUNTIME_ARN],
  })
);
```

Set `AGENTCORE_AGENT_RUNTIME_ARN` in your deployment environment or GitHub Actions secrets.

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Burn plan created
- `429 Too Many Requests`: Rate limit exceeded (includes Retry-After header)
- `502 Bad Gateway`: AgentCore error
- `503 Service Unavailable`: AgentCore not configured
- `504 Gateway Timeout`: Agent request timed out

## Next Steps

- [ ] Add DynamoDB integration for session storage
- [ ] Implement roast endpoint with session retrieval
- [ ] Add Cognito authentication
- [ ] Add request validation and sanitization
- [ ] Add comprehensive error logging
- [ ] Add metrics and monitoring
