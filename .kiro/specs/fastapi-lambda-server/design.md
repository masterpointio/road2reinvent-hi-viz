# Design Document

## Overview

This design implements a minimal FastAPI Lambda function for a hackathon. The solution uses a single Python Lambda that handles API routes through FastAPI. We're focusing on the happy path - just getting a health check endpoint working with the existing API Gateway.

## Architecture

### Simple Flow

```
Client → API Gateway → Lambda (FastAPI + Mangum) → Response
```

That's it. API Gateway already exists, we just add a Lambda function with FastAPI.

## Components and Interfaces

### CDK Stack Addition

First, add the Lambda import at the top of the stack file:

```typescript
import * as lambda from "aws-cdk-lib/aws-lambda";
```

Then add one Lambda function to the existing stack:

```typescript
const fastapiFunction = new lambda.Function(this, "FastAPIFunction", {
  runtime: lambda.Runtime.PYTHON_3_13,
  handler: "main.handler",
  code: lambda.Code.fromAsset("lib/lambda/fastapi", {
    bundling: {
      image: lambda.Runtime.PYTHON_3_13.bundlingImage,
      command: [
        "bash",
        "-c",
        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
      ],
    },
  }),
  timeout: cdk.Duration.seconds(29),
  memorySize: 512,
});
```

Add API Gateway integration:

```typescript
const apiResource = api.root.addResource("api");
const proxyResource = apiResource.addResource("{proxy+}");
proxyResource.addMethod(
  "ANY",
  new apigateway.LambdaIntegration(fastapiFunction)
);
```

Add stack output:

```typescript
new cdk.CfnOutput(this, "FastAPIUrl", {
  value: `${api.url}api/health`,
  description: "FastAPI Health Check URL",
});
```

### Python Application

**Directory Structure:**

```
lib/lambda/fastapi/
├── main.py              # Lambda handler
├── app.py               # FastAPI app with /health route
└── requirements.txt     # fastapi + mangum
```

**main.py** (Lambda handler):

```python
from mangum import Mangum
from app import app

handler = Mangum(app, api_gateway_base_path="/api")
```

**app.py** (FastAPI app):

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**requirements.txt**:

```
fastapi==0.115.0
mangum==0.18.0
```

## Data Models

### Health Check Response

```python
{
    "status": "healthy"
}
```

That's all we need for the hackathon.

## Correctness Properties

_A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees._

For this hackathon project, we're skipping formal property testing and focusing on getting it working.

## Error Handling

For the hackathon, we'll rely on FastAPI's built-in error handling:

- 404 for unknown routes (automatic)
- 500 for exceptions (automatic)
- Basic logging to CloudWatch (automatic with Lambda)

No custom error handling needed.

## Testing Strategy

For the hackathon, we'll skip automated tests and just manually verify the health endpoint works after deployment.

## Deployment

### Quick Deploy

```bash
npm run deploy
```

### Test It

```bash
curl <API_GATEWAY_URL>/api/health
# Should return: {"status":"healthy"}
```

## Future Extensibility

When you need to add more endpoints after the hackathon:

1. **Add route in app.py:**

```python
@app.get("/users")
def get_users():
    return {"users": []}
```

2. **Add Cognito auth (if needed):**

```typescript
// In CDK stack
const protectedResource = apiResource.addResource("users");
protectedResource.addMethod(
  "GET",
  new apigateway.LambdaIntegration(fastapiFunction),
  {
    authorizer: cognitoAuthorizer,
    authorizationType: apigateway.AuthorizationType.COGNITO,
  }
);
```

3. **Access user info in FastAPI:**

```python
from fastapi import Request

@app.get("/users")
def get_users(request: Request):
    # User info is in request.scope['aws.event']['requestContext']['authorizer']['claims']
    return {"users": []}
```

But for now, just get the health check working!
