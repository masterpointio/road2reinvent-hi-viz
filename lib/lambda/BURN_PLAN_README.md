# Burn Plan TypeScript Lambda

This Lambda function invokes the AgentCore Money Spender Agent to generate AWS spending burn plans.

## Endpoint

`POST /burn-plan`

## Request Body

```json
{
  "amount": "$2500",
  "timeline": 30,
  "stupidity": "Moderately stupid",
  "architecture": "mixed",
  "burning_style": "horizontal",
  "model_id": "optional-bedrock-model-id"
}
```

### Required Fields
- `amount`: Spending amount (string or number, e.g., "$2500" or 2500)
- `timeline`: Timeline in days (integer)
- `stupidity`: Efficiency level (string)
  - "Mildly dumb"
  - "Moderately stupid"
  - "Very stupid"
  - "Brain damage"

### Optional Fields
- `architecture`: Architecture type (default: "mixed")
  - "serverless"
  - "kubernetes"
  - "traditional"
  - "mixed"
- `burning_style`: Burning style (default: "horizontal")
  - "horizontal" - Spread spending evenly across timeline
  - "vertical" - Burst spending patterns
- `model_id`: Bedrock model ID (optional)

## Response

```json
{
  "status": "success",
  "analysis": {
    "total_amount": "$2500",
    "timeline_days": 30,
    "efficiency_level": "Moderately stupid",
    "services_deployed": [
      {
        "service_name": "EC2",
        "instance_type": "r7g.16xlarge",
        "quantity": 1,
        "start_day": 0,
        "end_day": 30,
        "duration_used": 30,
        "unit_cost": 3.2256,
        "total_cost": 2322.43,
        "usage_pattern": "24/7",
        "waste_factor": 0.85
      }
    ],
    "total_calculated_cost": 2500.00,
    "deployment_scenario": "...",
    "key_mistakes": ["..."],
    "recommendations": ["..."]
  }
}
```

## Error Response

```json
{
  "error": "Error message",
  "status": "error"
}
```

## Environment Variables

- `AGENTCORE_AGENT_RUNTIME_ARN`: AgentCore agent runtime ARN (required)
- `AWS_REGION`: AWS region (default: "us-east-1")

## IAM Permissions Required

The Lambda execution role needs:
```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock-agentcore:InvokeAgentRuntime"
  ],
  "Resource": "*"
}
```

## Example Usage

```bash
curl -X POST https://your-api.execute-api.us-east-1.amazonaws.com/prod/burn-plan \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "$2500",
    "timeline": 30,
    "stupidity": "Moderately stupid",
    "architecture": "serverless",
    "burning_style": "horizontal"
  }'
```

## Differences from Python FastAPI Lambda

- **Direct endpoint**: `/burn-plan` (not under `/api`)
- **Simplified**: Does not proxy all requests, only handles burn plan generation
- **TypeScript**: Uses AWS SDK v3 for Node.js
- **Standalone**: Independent Lambda function, not part of FastAPI proxy
