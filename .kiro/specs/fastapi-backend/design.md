# Design Document: FastAPI Backend

## Overview

This design adds a Python FastAPI backend to the existing CDK infrastructure. The API will be deployed as a containerized Lambda function using Docker, allowing us to use Python with FastAPI while maintaining the existing TypeScript CDK stack. The API will be integrated with the existing API Gateway and will initially provide a simple "hello world" endpoint to validate the infrastructure.

## Architecture

### High-Level Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Lambda Function     │
│  (Docker Container)  │
│  ┌────────────────┐  │
│  │  Mangum        │  │
│  │  Adapter       │  │
│  └────────┬───────┘  │
│           │          │
│  ┌────────▼───────┐  │
│  │  FastAPI App   │  │
│  └────────────────┘  │
└──────────────────────┘
```

### Component Interaction Flow

1. Client sends HTTP request to API Gateway
2. API Gateway invokes Lambda function with AWS Lambda event
3. Mangum adapter converts Lambda event to ASGI format
4. FastAPI application processes the request
5. FastAPI returns response to Mangum
6. Mangum converts response to Lambda format
7. API Gateway returns HTTP response to client

## Components and Interfaces

### 1. FastAPI Application (`lib/lambda/fastapi-app/app.py`)

**Responsibilities:**

- Define API routes and endpoints
- Handle HTTP requests and responses
- Provide application logic

**Interface:**

```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# Endpoints
@app.get("/api/hello")
async def hello() -> dict

# Lambda handler
handler = Mangum(app)
```

### 2. Mangum Adapter

**Responsibilities:**

- Convert AWS Lambda events to ASGI format
- Convert ASGI responses to Lambda response format
- Handle API Gateway proxy integration

**Interface:**

- Input: AWS Lambda event and context
- Output: Lambda response dictionary

### 3. Docker Container

**Responsibilities:**

- Package FastAPI application and dependencies
- Provide Python runtime environment
- Use AWS Lambda Python base image (supports ARM64)

**Structure:**

```
lib/lambda/fastapi-app/
├── app.py              # FastAPI application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition
└── .dockerignore       # Files to exclude from build (optional but recommended)
```

### 4. CDK Lambda Function Construct

**Responsibilities:**

- Define Lambda function using Docker image
- Configure function settings (memory, timeout)
- Set up IAM permissions
- Integrate with API Gateway

**Interface:**

```typescript
const fastApiFunction = new lambda.DockerImageFunction(this, 'FastApiFunction', {
  code: lambda.DockerImageCode.fromImageAsset(path),
  memorySize: 512,
  timeout: Duration.seconds(30),
  environment: { ... }
});
```

### 5. API Gateway Integration

**Responsibilities:**

- Route HTTP requests to Lambda function
- Handle CORS preflight requests
- Provide public endpoint URL

**Interface:**

- Extends existing API Gateway RestApi (defined in r2r-stack.ts)
- Adds `/api` resource with `{proxy+}` child resource
- Routes all `/api/*` requests to FastAPI Lambda function
- Leverages existing CORS configuration on the API Gateway

## Data Models

### Request/Response Models

#### Hello Endpoint Response

```python
{
  "message": str
}
```

### Lambda Event Structure

The Mangum adapter handles conversion, but for reference:

```json
{
  "httpMethod": "GET",
  "path": "/api/hello",
  "headers": { ... },
  "body": null,
  "isBase64Encoded": false
}
```

### Lambda Response Structure

```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"message\": \"Hello World\"}"
}
```

## Correctness Properties

_A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees._

### Testable Properties

Most of the acceptance criteria for this feature relate to infrastructure configuration and deployment processes, which are validated through CDK synthesis and deployment rather than runtime property testing. However, we can define example-based tests for the functional behavior of the API:

**Example 1: Hello endpoint returns success**
The /api/hello endpoint should return a 200 status code with a JSON response containing a message field.
**Validates: Requirements 2.1, 2.2**

**Example 2: Lambda handler processes events**
When the Lambda handler receives an API Gateway proxy event, it should successfully process the request and return a valid Lambda response.
**Validates: Requirements 1.3, 3.3**

**Example 3: Endpoint registration**
The FastAPI application should have the /api/hello route registered in its route list.
**Validates: Requirements 2.3**

### Infrastructure Validation

The following requirements are validated through CDK synthesis and deployment testing rather than runtime properties:

- Requirements 1.1, 1.2, 1.4 (Docker packaging and CDK outputs)
- Requirements 3.1, 3.2 (Dependency versions and Docker build)
- Requirements 4.1, 4.2, 4.3, 4.4 (CDK resource definitions)

## Error Handling

### Application-Level Errors

**FastAPI Exception Handling:**

- FastAPI automatically handles common HTTP errors (404, 405, 422)
- Returns JSON error responses with appropriate status codes
- Includes error details in response body

**Lambda Execution Errors:**

- Mangum adapter catches and converts Python exceptions to Lambda error responses
- Lambda service handles timeout and memory errors
- CloudWatch Logs capture all error traces

### CORS Error Handling

**Preflight Failures:**

- Missing or invalid CORS headers result in browser blocking the request
- API Gateway handles preflight requests automatically via CORS configuration

### Error Response Format

```python
{
  "detail": str,  # Error message
  "status_code": int  # HTTP status code
}
```

## Testing Strategy

### Unit Testing

**Framework:** pytest

**Test Coverage:**

1. **Endpoint Tests**

   - Test /api/hello endpoint returns correct response structure
   - Test response includes required fields
   - Test status codes are correct

2. **Integration Tests**
   - Test Mangum adapter converts Lambda events correctly
   - Test FastAPI app initializes with correct configuration
   - Test Lambda handler returns valid response format

**Test Utilities:**

- Use FastAPI's TestClient for endpoint testing
- Mock Lambda events for integration testing
- Use pytest fixtures for app initialization

### Property-Based Testing

Given the minimal scope of this feature (single hello world endpoint), property-based testing is not applicable. The acceptance criteria are primarily infrastructure-related or example-based functional tests. As the API grows with more complex business logic, property-based tests should be added for:

- Input validation across ranges of values
- Data transformation consistency
- State management properties

### Manual Testing

**Local Testing:**

1. Run FastAPI app locally with `uvicorn app:app --reload`
2. Access interactive API docs at `http://localhost:8000/docs`
3. Test `/api/hello` endpoint using curl, Postman, or the interactive docs
4. Note: CORS is handled by API Gateway in production, not locally

**Deployed Testing:**

1. Deploy CDK stack to AWS
2. Test API Gateway endpoint URL
3. Verify Lambda function logs in CloudWatch
4. Test CORS from frontend application

### CDK Testing

**Snapshot Tests:**

- Verify CDK synthesizes expected CloudFormation template
- Ensure Lambda function has correct configuration
- Validate API Gateway integration settings

**Assertion Tests:**

- Assert Lambda function uses Docker image
- Assert API Gateway has CORS configured
- Assert outputs include API endpoint URL

## Implementation Notes

### Docker Image Optimization

**Base Image:**

- Use `public.ecr.aws/lambda/python:3.12` as base image
- This is AWS's official Lambda Python runtime image
- Includes Lambda Runtime Interface Client (RIC)

**Layer Caching:**

- Copy requirements.txt first and install dependencies
- Copy application code last to maximize cache hits
- Reduces rebuild time during development

**Image Size:**

- Keep dependencies minimal
- Only include FastAPI and Mangum
- Lambda has 10GB image size limit (plenty of headroom)

### CDK Integration

**Integration with Existing Stack:**

The FastAPI Lambda will be added to the existing `R2RStack` in `lib/r2r-stack.ts`:

1. Create `DockerImageFunction` for FastAPI (similar to existing `NodejsFunction`)
2. Reference the existing `api` RestApi resource
3. Add `/api` resource to the API Gateway
4. Add `{proxy+}` child resource to forward all `/api/*` paths
5. Create `LambdaIntegration` connecting the proxy resource to FastAPI Lambda
6. CORS is already configured on the API Gateway, no changes needed

**Resource Naming:**

- Use consistent naming convention: `FastApi*`
- Follow existing pattern from NodeJS Lambda (`HelloWorldFunction`)
- Function name: `fastapi-function`

**API Gateway Routing:**

- Existing: `/hello` → NodeJS Lambda (with Cognito auth)
- New: `/api/{proxy+}` → FastAPI Lambda (no auth initially)
- FastAPI handles internal routing for all `/api/*` paths
- This allows adding new FastAPI endpoints without CDK changes

**Environment Variables:**

- Pass configuration through Lambda environment variables
- Include stage/environment identifier
- Add any future database connection strings

### Development Workflow

**Local Development:**

1. Develop FastAPI app locally with hot reload
2. Test endpoints using FastAPI's interactive docs (`/docs`)
3. Build Docker image locally to verify
4. Deploy to AWS for integration testing

**Deployment:**

1. CDK builds Docker image automatically during synthesis
2. Pushes image to ECR (Elastic Container Registry)
3. Updates Lambda function with new image
4. No manual Docker commands needed

### Future Considerations

As the API grows beyond this initial hello world implementation, consider:

**Authentication:**

- Integrate with existing Cognito User Pool
- Add JWT token validation middleware

**Database:**

- Add DynamoDB or RDS connection
- Implement data models with Pydantic

**Monitoring:**

- Add structured logging with correlation IDs
- Implement custom CloudWatch metrics

**API Versioning:**

- Use path-based versioning: `/api/v1/`, `/api/v2/`

## Dependencies

### Python Dependencies (requirements.txt)

```
fastapi==0.115.0
mangum==0.18.0
uvicorn==0.32.0  # For local development only
```

### CDK Dependencies

No new CDK dependencies required. The existing `aws-cdk-lib` includes:

- `aws-lambda` for Lambda function construct
- `aws-apigateway` for API Gateway integration
- `aws-ecr-assets` for Docker image building

### Development Dependencies

```
pytest==8.3.0
pytest-asyncio==0.24.0
httpx==0.27.0  # For TestClient
```

## Deployment Configuration

### Lambda Function Settings

```typescript
{
  memorySize: 512,  // MB - sufficient for FastAPI
  timeout: 29,      // seconds - API Gateway max timeout
  architecture: Architecture.ARM_64,  // Graviton2 for cost savings (Python 3.12 supports ARM64)
  environment: {
    STAGE: 'prod',
    LOG_LEVEL: 'INFO'
  }
}
```

### API Gateway Settings

```typescript
{
  proxy: true,  // Forward all paths to Lambda
  defaultCorsPreflightOptions: {
    allowOrigins: ['*'],  // Update to specific origins in production
    allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowHeaders: ['Content-Type', 'Authorization']
  }
}
```

### Docker Build Settings

**Dockerfile:**

```dockerfile
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["app.handler"]
```

**.dockerignore:**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db

# Git
.git/
.gitignore

# Documentation
README.md
*.md
```

## Security Considerations

### CORS Configuration

- Configured at API Gateway level to allow all origins (`*`)
- Inherits existing CORS configuration from the API Gateway
- Can be restricted to specific domains later if needed

### Lambda Permissions

- Lambda execution role needs minimal permissions
- CloudWatch Logs write access (automatic)
- No additional AWS service access needed for hello world

### API Gateway

- Currently no authentication on FastAPI endpoints
- Future: integrate with Cognito authorizer
- Consider API keys or usage plans for rate limiting

### Docker Image

- Use official AWS Lambda base images
- Keep dependencies up to date
- Scan for vulnerabilities in CI/CD pipeline

## Monitoring and Observability

### CloudWatch Logs

- Lambda automatically logs to CloudWatch
- Log group: `/aws/lambda/fastapi-function`
- Includes FastAPI application logs
- Mangum adapter logs request/response details

### CloudWatch Metrics

**Lambda Metrics:**

- Invocations
- Duration
- Errors
- Throttles
- Concurrent executions

**API Gateway Metrics:**

- Request count
- Latency (integration and total)
- 4XX and 5XX errors

### Alarms

**Recommended Alarms:**

- Lambda error rate > 5%
- Lambda duration > 25 seconds (approaching timeout)
- API Gateway 5XX errors > 10 in 5 minutes

### Tracing

- Enable AWS X-Ray for distributed tracing
- Trace requests through API Gateway → Lambda → FastAPI
- Identify performance bottlenecks

## Rollback Strategy

### Deployment Rollback

- CDK maintains previous stack state
- Use `cdk deploy --rollback` to revert
- Lambda versions allow traffic shifting

### Blue/Green Deployment

- Future enhancement: use Lambda aliases
- Route percentage of traffic to new version
- Automatic rollback on CloudWatch alarms

### Database Migrations

- Not applicable for hello world
- Future: use migration tools (Alembic)
- Always backward compatible migrations
