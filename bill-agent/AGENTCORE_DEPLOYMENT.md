# Money Spender Agent - AgentCore Deployment Guide

This guide explains how to deploy the Money Spender Agent to AWS Bedrock AgentCore Runtime.

## Prerequisites

1. **AWS CLI configured** with appropriate credentials
2. **Python 3.10+** installed
3. **AgentCore CLI** installed:
   ```bash
   pip install bedrock-agentcore-starter-toolkit
   ```

## Deployment Steps

### 1. Install Dependencies

```bash
cd agent
pip install -r requirements.txt
```

### 2. Configure the Agent

```bash
agentcore configure \
  --entrypoint agentcore_handler.py \
  --name money-spender-agent \
  --runtime PYTHON_3_12 \
  --requirements-file requirements.txt \
  --region us-west-2 \
  --non-interactive
```

**Configuration Options:**
- `--entrypoint`: The AgentCore handler file (agentcore_handler.py)
- `--name`: Agent name in AgentCore
- `--runtime`: Python runtime version
- `--requirements-file`: Dependencies file
- `--region`: AWS region for deployment
- `--non-interactive`: Skip prompts and use defaults

**Optional Flags:**
- `--disable-memory`: Skip memory setup if not needed
- `--execution-role`: Specify custom IAM execution role ARN
- `--vpc`: Enable VPC networking (requires --subnets and --security-groups)

### 3. Deploy to AWS

```bash
agentcore launch
```

This will:
- Package your agent code
- Create necessary AWS resources (Lambda, API Gateway, etc.)
- Deploy to AgentCore Runtime
- Return an endpoint URL

**Deployment Options:**
- `--local`: Build and run locally for testing (requires Docker)
- `--local-build`: Build locally and deploy to cloud
- `--env KEY=VALUE`: Set environment variables

### 4. Test the Deployed Agent

#### Basic Test
```bash
agentcore invoke '{
  "amount": "$2500",
  "timeline": 30,
  "stupidity": "Moderately stupid",
  "architecture": "serverless",
  "burning_style": "horizontal"
}'
```

#### Test with Different Parameters
```bash
# Kubernetes with vertical bursts
agentcore invoke '{
  "amount": "$5000",
  "timeline": 45,
  "stupidity": "Very stupid",
  "architecture": "kubernetes",
  "burning_style": "vertical"
}'

# Traditional with horizontal spending
agentcore invoke '{
  "amount": "$1000",
  "timeline": 14,
  "stupidity": "Mildly dumb",
  "architecture": "traditional",
  "burning_style": "horizontal"
}'

# Brain damage with mixed architecture
agentcore invoke '{
  "amount": "$10000",
  "timeline": 60,
  "stupidity": "Brain damage",
  "architecture": "mixed",
  "burning_style": "vertical"
}'
```

### 5. Check Agent Status

```bash
agentcore status --verbose
```

This shows:
- Agent configuration
- Deployment status
- Endpoint URL
- Resource details

### 6. Manage Sessions

```bash
# Stop a specific session
agentcore stop-session --session-id <session-id>

# Stop all sessions for the agent
agentcore stop-session
```

## Request Payload Format

The agent expects a JSON payload with the following fields:

```json
{
  "amount": "$2500",           // Required: Amount spent (string with currency symbol)
  "timeline": 30,              // Required: Timeline in days (integer)
  "stupidity": "Moderately stupid",  // Required: Efficiency level
  "architecture": "serverless", // Required: Architecture type
  "burning_style": "horizontal", // Required: Burning style
  "model_id": "amazon.nova-lite-v1:0"  // Optional: Bedrock model ID
}
```

### Valid Values

**stupidity** (Efficiency Level):
- `"Mildly dumb"` - Rookie mistakes, minor over-provisioning
- `"Moderately stupid"` - Significant over-provisioning, wasteful patterns
- `"Very stupid"` - Extreme over-engineering, architectural disasters
- `"Brain damage"` - Maximum over-engineering with obscure services

**architecture** (Architecture Type):
- `"serverless"` - Lambda, API Gateway, DynamoDB, Step Functions, etc.
- `"kubernetes"` - EKS, ECR, container instances, load balancers
- `"traditional"` - EC2, RDS, EBS, ELB, classic infrastructure
- `"mixed"` - Chaotic combination of all architecture types

**burning_style** (Spending Pattern):
- `"horizontal"` - Regular spending spread over entire timeline
- `"vertical"` - Burst spending with services spinning up/down at different times

## Response Format

The agent returns a JSON response with the following structure:

```json
{
  "status": "success",
  "analysis": {
    "total_amount": "$2500",
    "timeline_days": 30,
    "efficiency_level": "Moderately stupid",
    "architecture_type": "serverless",
    "burning_style": "horizontal",
    "services_deployed": [
      {
        "service_name": "Lambda",
        "instance_type": "Provisioned Concurrency",
        "quantity": 10,
        "unit_cost": 0.00001667,
        "total_cost": 1200.0,
        "start_day": 0,
        "end_day": 30,
        "duration_used": "entire timeline",
        "usage_pattern": "Running 24/7",
        "waste_factor": "Over-provisioned for minimal workloads"
      }
    ],
    "total_calculated_cost": 2450.0,
    "deployment_scenario": "Detailed narrative...",
    "key_mistakes": ["Mistake 1", "Mistake 2", ...],
    "recommendations": ["Recommendation 1", "Recommendation 2", ...],
    "roast": "Brutal roast of the wasteful spending..."
  }
}
```

## Integration with API Gateway

Once deployed, you can invoke the agent via HTTP:

```bash
# Get the endpoint URL
ENDPOINT=$(agentcore status --verbose | grep -o 'https://[^"]*')

# Invoke via curl
curl -X POST "$ENDPOINT/invocations" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "$2500",
    "timeline": 30,
    "stupidity": "Moderately stupid",
    "architecture": "serverless",
    "burning_style": "horizontal"
  }'
```

## Environment Variables

You can set environment variables during deployment:

```bash
agentcore launch --env MONEY_SPENDER_MODEL=amazon.nova-pro-v1:0
```

Available environment variables:
- `MONEY_SPENDER_MODEL`: Bedrock model ID (default: amazon.nova-lite-v1:0)

## Updating the Agent

To update the deployed agent:

```bash
# Make your code changes
# Then redeploy
agentcore launch --auto-update-on-conflict
```

## Cleanup

To remove the deployed agent and all associated resources:

```bash
agentcore destroy
```

Options:
- `--dry-run`: Show what would be destroyed without actually destroying
- `--force`: Skip confirmation prompts
- `--delete-ecr-repo`: Also delete the ECR repository

## Troubleshooting

### Check Logs
```bash
# View CloudWatch logs
aws logs tail /aws/lambda/money-spender-agent --follow
```

### Local Testing
Before deploying to AWS, test locally:

```bash
# Build and run locally
agentcore launch --local

# In another terminal, invoke locally
agentcore invoke '{"amount": "$1000", "timeline": 30, "stupidity": "Mildly dumb", "architecture": "traditional", "burning_style": "horizontal"}' --local
```

### Common Issues

1. **Missing bedrock-agentcore**: Ensure it's in requirements.txt
2. **Import errors**: Check that all dependencies are listed
3. **Timeout errors**: Increase Lambda timeout in configuration
4. **Memory errors**: Increase Lambda memory allocation

## Cost Considerations

AgentCore Runtime costs include:
- Lambda execution time
- API Gateway requests
- CloudWatch logs storage
- Bedrock model invocations

Estimated cost for moderate usage: $5-20/month

## Security

- Agent runs in your AWS account
- Uses IAM roles for permissions
- Supports VPC networking for private deployments
- Can integrate with OAuth for authentication

## Next Steps

1. Deploy the agent following the steps above
2. Test with various parameters
3. Integrate with your frontend application
4. Set up monitoring and alerts
5. Configure auto-scaling if needed
