# AgentCore IAM Authentication Setup

This document explains how the FastAPI Lambda uses IAM authentication to invoke AgentCore agents.

## Overview

Instead of using API keys, the Lambda function uses AWS IAM credentials to authenticate with AgentCore. This provides better security through:

- **No secrets management**: Credentials are automatically provided by the Lambda execution role
- **Fine-grained permissions**: IAM policies control exactly which agents can be invoked
- **Audit trail**: All invocations are logged in CloudTrail
- **Automatic rotation**: No manual credential rotation needed

## Architecture

```
┌─────────────────┐
│  FastAPI Lambda │
│                 │
│  Execution Role │──────┐
│  with IAM perms │      │
└─────────────────┘      │
                         │ IAM Auth
                         ▼
                  ┌──────────────┐
                  │  AgentCore   │
                  │    Agent     │
                  │  (via ARN)   │
                  └──────────────┘
```

## Required Environment Variables

### AGENTCORE_AGENT_RUNTIME_ARN
The ARN of your AgentCore agent runtime. Format:
```
arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/agent_name-XXXXX
```

Example:
```
arn:aws:bedrock-agentcore:us-east-1:114713347049:runtime/money_spender_aws_agent-GIJFH89w3J
```

### AWS_REGION
The AWS region where your agent is deployed. This is automatically set by Lambda.

## IAM Permissions

The Lambda execution role needs the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:InvokeAgentRuntime"
      ],
      "Resource": "arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/agent_name-XXXXX"
    }
  ]
}
```

This is automatically configured in the CDK stack:

```typescript
fastapiFunction.addToRolePolicy(
  new iam.PolicyStatement({
    effect: iam.Effect.ALLOW,
    actions: ['bedrock-agentcore:InvokeAgentRuntime'],
    resources: [process.env.AGENTCORE_AGENT_RUNTIME_ARN],
  })
);
```

## AgentCore Client Initialization

The client automatically uses IAM credentials from the Lambda execution role:

```python
from utils.agentcore_client import AgentCoreClient

# Credentials are automatically obtained from Lambda execution role
client = AgentCoreClient(
    agent_runtime_arn="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/agent_name-XXXXX",
    region="us-east-1"
)
```

The client uses boto3's `bedrock-agentcore` service to invoke the agent:

```python
import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='us-east-1')

payload = json.dumps({
    "prompt": "Generate burn plan",
    "amount": "$3000",
    "timeline": 30
})

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/agent_name-XXXXX',
    runtimeSessionId='unique-session-id-33-chars-minimum',
    payload=payload,
    qualifier="DEFAULT"
)
```

## Deployment

1. **Set the agent runtime ARN** in your deployment environment:
   ```bash
   export AGENTCORE_AGENT_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/agent_name-XXXXX"
   ```

2. **Deploy the CDK stack**:
   ```bash
   npm run cdk deploy
   ```

3. **Verify permissions** by checking the Lambda execution role in the AWS Console

## Testing

Test the health endpoint to verify AgentCore is configured:

```bash
curl https://your-api-gateway-url/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "agentcore_configured": true
}
```

## Troubleshooting

### Error: "AGENTCORE_AGENT_RUNTIME_ARN is required"
- Ensure the environment variable is set in the CDK stack
- Check that `process.env.AGENTCORE_AGENT_RUNTIME_ARN` is defined during deployment

### Error: "Access Denied" or "UnauthorizedException"
- Verify the Lambda execution role has the correct IAM permissions
- Check that the agent runtime ARN in the policy matches the environment variable
- Ensure the action is `bedrock-agentcore:InvokeAgentRuntime` (not `bedrock:InvokeAgent`)
- Ensure the agent runtime exists in the specified region

### Error: "Failed to initialize AgentCore client"
- Check CloudWatch Logs for detailed error messages
- Ensure `boto3` is available (it's included by default in Lambda)
- Verify the boto3 version supports the `bedrock-agentcore` service

### Error: "Session ID must be at least 33 characters"
- The client automatically generates session IDs with UUID format
- Session IDs are in format: `{uuid}-{uuid-prefix}` (e.g., `550e8400-e29b-41d4-a716-446655440000-a1b2c`)

## Security Best Practices

1. **Least privilege**: Only grant permissions to the specific agent ARN needed
2. **Resource-based policies**: Consider adding resource-based policies to the agent for additional security
3. **Monitoring**: Enable CloudTrail logging for agent invocations
4. **Rotation**: If you need to change agents, update the ARN and redeploy

## API Usage

The AgentCore client wraps the boto3 `bedrock-agentcore` service:

### Invoke Agent Runtime

```python
import json
import uuid

# Generate session ID (must be 33+ characters)
session_id = str(uuid.uuid4()) + "-" + str(uuid.uuid4())[:5]

# Build payload
payload = json.dumps({
    "prompt": "Generate AWS spending burn plan",
    "amount": "$3000",
    "timeline": 30,
    "stupidity": "Brain damage",
    "architecture": "kubernetes",
    "burning_style": "vertical"
})

# Invoke agent
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:114713347049:runtime/money_spender_aws_agent-GIJFH89w3J',
    runtimeSessionId=session_id,
    payload=payload,
    qualifier="DEFAULT"
)

# Parse response
response_body = response['response'].read()
response_data = json.loads(response_body)
```

### Session ID Requirements

- Must be at least 33 characters long
- Should be unique per invocation
- Format: `{uuid}-{uuid-prefix}` ensures uniqueness and length requirement
