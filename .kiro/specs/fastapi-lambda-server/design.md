# Design Document

## Overview

This design implements a FastAPI Lambda function that acts as a proxy between the frontend and AgentCore backend for the AWS Bill Burner application. The Lambda provides REST API endpoints for generating AWS spending burn plans and roast commentary using Strands agents via the AgentCore SDK. The architecture follows a layered approach with routers, services, and client wrappers to ensure clean separation of concerns and robust error handling.

## Architecture

### Request Flow

```
Client → API Gateway → Lambda (FastAPI + Mangum) → Router → Service → AgentCore Client → Strands Agent
                                                                                              ↓
Client ← API Gateway ← Lambda Response ← Router ← Service ← AgentCore Client ← Structured Output
```

### Component Layers

1. **Router Layer**: FastAPI route handlers that validate requests and handle HTTP concerns
2. **Service Layer**: Business logic for burn plan generation and roast commentary
3. **Client Layer**: AgentCore SDK wrapper with retry logic and error handling
4. **Agent Layer**: Strands agents that generate structured responses

## Components and Interfaces

### CDK Stack Configuration

The Lambda function is configured with:
- Python 3.13 runtime
- 29 second timeout (just under API Gateway's 30s limit)
- 512MB memory
- Environment variables: `AGENTCORE_API_KEY`, `STRANDS_AGENT_ENDPOINT`
- CDK bundling for pip dependencies

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
  environment: {
    AGENTCORE_API_KEY: process.env.AGENTCORE_API_KEY || "",
    STRANDS_AGENT_ENDPOINT: process.env.STRANDS_AGENT_ENDPOINT || "",
  },
});
```

### Directory Structure

```
lib/lambda/fastapi/
├── main.py                      # Lambda handler with Mangum
├── app.py                       # FastAPI application
├── models.py                    # Pydantic models
├── requirements.txt             # Python dependencies
├── routers/
│   ├── __init__.py
│   ├── burn_plan.py            # Burn plan endpoint
│   └── roast.py                # Roast endpoint
├── services/
│   ├── __init__.py
│   └── strands_service.py      # Strands agent service
└── utils/
    ├── __init__.py
    └── agentcore_client.py     # AgentCore SDK wrapper
```

### AgentCore Client Wrapper

The `AgentCoreClient` class wraps the AgentCore SDK with:

**Initialization:**
```python
class AgentCoreClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 2
    ):
        self.api_key = api_key or os.environ.get("AGENTCORE_API_KEY")
        self.endpoint = endpoint or os.environ.get("STRANDS_AGENT_ENDPOINT")
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Validate configuration
        if not self.api_key:
            raise AgentCoreError("AGENTCORE_API_KEY is required")
        if not self.endpoint:
            raise AgentCoreError("STRANDS_AGENT_ENDPOINT is required")
            
        # Initialize SDK client
        self.client = agentcore.Client(
            api_key=self.api_key,
            endpoint=self.endpoint
        )
```

**Retry Logic:**
```python
def _invoke_agent(self, task_name, instructions, parameters):
    for attempt in range(self.max_retries + 1):
        try:
            response = self.client.invoke_task(
                task_name=task_name,
                instructions=instructions,
                parameters=parameters,
                timeout=self.timeout
            )
            return response
        except TimeoutError:
            if attempt < self.max_retries:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
                continue
            raise AgentTimeoutError(...)
        except Exception as e:
            # Handle rate limits, connection errors, etc.
            ...
```

**Custom Exceptions:**
- `AgentCoreError`: Base exception
- `AgentTimeoutError`: Timeout errors (504)
- `AgentRateLimitError`: Rate limit errors (429)
- `AgentConnectionError`: Connection failures (502)

### Strands Service Layer

The `StrandsService` class provides business logic:

**Burn Plan Generation:**
```python
class StrandsService:
    def generate_burn_plan(self, config: BurnConfig) -> BurnPlan:
        # Convert config to dict
        config_dict = {
            "amount": config.amount,
            "timeline": config.timeline,
            "stupidity": config.stupidity,
            "architecture": config.architecture,
            "burning_style": config.burning_style
        }
        
        # Invoke agent
        response = self.client.generate_burn_plan(config_dict)
        
        # Parse and validate
        burn_plan = BurnPlan(**response)
        
        # Validate cost match (within 10%)
        self._validate_cost_match(config.amount, burn_plan.total_calculated_cost)
        
        return burn_plan
```

**Roast Generation:**
```python
def generate_roast(self, burn_plan: BurnPlan) -> str:
    context = {
        "total_amount": burn_plan.total_amount,
        "services": [
            {
                "service_name": svc.service_name,
                "total_cost": svc.total_cost,
                "waste_factor": svc.waste_factor
            }
            for svc in burn_plan.services_deployed
        ],
        "stupidity_level": burn_plan.efficiency_level
    }
    
    roast_text = self.client.generate_roast(context)
    return roast_text
```

### Router Layer

**Burn Plan Router:**
```python
@router.post("", response_model=BurnPlanResponse, status_code=201)
async def create_burn_plan(
    request: BurnPlanRequest,
    strands_service: StrandsService = Depends(get_strands_service)
) -> BurnPlanResponse:
    try:
        burn_plan = strands_service.generate_burn_plan(request.config)
        session_id = str(uuid.uuid4())
        
        # TODO: Store in DynamoDB
        
        return BurnPlanResponse(
            session_id=session_id,
            burn_plan=burn_plan
        )
    except AgentTimeoutError:
        raise HTTPException(status_code=504, detail="...")
    except AgentRateLimitError as e:
        raise HTTPException(
            status_code=429,
            detail="...",
            headers={"Retry-After": str(e.retry_after)}
        )
    except AgentCoreError:
        raise HTTPException(status_code=502, detail="...")
```

**Dependency Injection:**
```python
def get_agentcore_client() -> AgentCoreClient:
    try:
        return AgentCoreClient()
    except AgentCoreError as e:
        raise HTTPException(status_code=503, detail=f"...")

def get_strands_service(
    client: AgentCoreClient = Depends(get_agentcore_client)
) -> StrandsService:
    return StrandsService(client)
```

### FastAPI Application

**Main Application:**
```python
app = FastAPI(
    title="AWS Bill Burner API",
    description="API for generating AWS spending burn plans",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(burn_plan.router)
app.include_router(roast.router)

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    agentcore_configured = bool(
        os.environ.get("AGENTCORE_API_KEY") and
        os.environ.get("STRANDS_AGENT_ENDPOINT")
    )
    return HealthResponse(
        status="healthy",
        agentcore_configured=agentcore_configured
    )
```

## Data Models

### Request Models

**BurnConfig:**
```python
class BurnConfig(BaseModel):
    amount: str  # e.g., "$1000" or "₹50000"
    timeline: int  # Days, must be > 0
    stupidity: Literal["Mildly dumb", "Moderately stupid", "Very stupid", "Brain damage"]
    architecture: Literal["serverless", "kubernetes", "traditional", "mixed"]
    burning_style: Literal["horizontal", "vertical"]
```

**BurnPlanRequest:**
```python
class BurnPlanRequest(BaseModel):
    config: BurnConfig
```

**RoastRequest:**
```python
class RoastRequest(BaseModel):
    session_id: str
```

### Response Models

**ServiceCost:**
```python
class ServiceCost(BaseModel):
    service_name: str
    instance_type: Optional[str]
    quantity: int
    start_day: int
    end_day: int
    duration_used: int
    unit_cost: float
    total_cost: float
    usage_pattern: Optional[str]
    waste_factor: Optional[str]
```

**BurnPlan:**
```python
class BurnPlan(BaseModel):
    total_amount: str
    timeline_days: int
    efficiency_level: str
    services_deployed: List[ServiceCost]
    total_calculated_cost: float
    deployment_scenario: str
    key_mistakes: List[str]
    recommendations: List[str]
```

**BurnPlanResponse:**
```python
class BurnPlanResponse(BaseModel):
    session_id: str
    burn_plan: BurnPlan
```

**RoastResponse:**
```python
class RoastResponse(BaseModel):
    roast_text: str
```

**HealthResponse:**
```python
class HealthResponse(BaseModel):
    status: str
    agentcore_configured: bool
```

## Correctness Properties

_A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees._

### Property 1: Cost Validation Tolerance
*For any* burn plan with a requested amount and calculated cost, the calculated cost should be within 10% of the requested amount (or validation should be skipped if amount cannot be parsed).
**Validates: Requirements 15.2, 15.3**

### Property 2: Retry Exponential Backoff
*For any* agent invocation that fails with a retryable error, the wait time before retry N should equal 2^N seconds.
**Validates: Requirements 9.2**

### Property 3: Environment Variable Validation
*For any* AgentCore client initialization, if either AGENTCORE_API_KEY or STRANDS_AGENT_ENDPOINT is missing, an AgentCoreError should be raised.
**Validates: Requirements 8.1, 8.2**

### Property 4: HTTP Status Code Mapping
*For any* AgentCore error type, the corresponding HTTP status code should be: AgentTimeoutError → 504, AgentRateLimitError → 429, AgentConnectionError → 502, AgentCoreError → 502, initialization errors → 503.
**Validates: Requirements 12.1, 12.2, 12.3, 13.5**

### Property 5: Session ID Uniqueness
*For any* burn plan creation, the generated session ID should be a valid UUID v4 format.
**Validates: Requirements 13.3**

## Error Handling

### Error Hierarchy

```
AgentCoreError (base)
├── AgentTimeoutError (504 Gateway Timeout)
├── AgentRateLimitError (429 Too Many Requests)
│   └── retry_after: Optional[int]
└── AgentConnectionError (502 Bad Gateway)
```

### HTTP Status Code Mapping

| Error Type | HTTP Status | Description |
|------------|-------------|-------------|
| AgentTimeoutError | 504 | Agent invocation exceeded timeout |
| AgentRateLimitError | 429 | Rate limit exceeded, includes Retry-After header |
| AgentConnectionError | 502 | Failed to connect to AgentCore |
| AgentCoreError | 502 | Generic agent error |
| Initialization Error | 503 | AgentCore client not configured |
| Validation Error | 422 | Invalid request data (FastAPI automatic) |
| Not Found | 404 | Session not found |

### Retry Strategy

**Retryable Errors:**
- TimeoutError
- Connection errors

**Non-Retryable Errors:**
- Rate limit errors (return immediately with 429)
- Validation errors
- Invalid responses

**Retry Logic:**
```
Attempt 1: Immediate
Attempt 2: Wait 2^0 = 1 second
Attempt 3: Wait 2^1 = 2 seconds
Max attempts: 3 (initial + 2 retries)
```

### Error Response Format

All errors return JSON:
```json
{
  "detail": "Error message"
}
```

Rate limit errors include header:
```
Retry-After: 60
```

## Testing Strategy

### Unit Testing

**Test Coverage:**
- AgentCore client initialization with valid/invalid config
- Retry logic with exponential backoff
- Error type mapping to HTTP status codes
- Cost validation within tolerance
- Pydantic model validation

**Test Framework:** pytest

**Example Tests:**
```python
def test_agentcore_client_missing_api_key():
    with pytest.raises(AgentCoreError, match="AGENTCORE_API_KEY is required"):
        AgentCoreClient(api_key=None, endpoint="http://test")

def test_cost_validation_within_tolerance():
    service = StrandsService(mock_client)
    # Should not raise for $1000 requested, $950 calculated
    service._validate_cost_match("$1000", 950.0)

def test_cost_validation_outside_tolerance():
    service = StrandsService(mock_client)
    with pytest.raises(AgentCoreError, match="Cost mismatch"):
        service._validate_cost_match("$1000", 800.0)
```

### Integration Testing

**Manual Testing:**
1. Deploy stack with valid AgentCore credentials
2. Test health endpoint: `GET /api/health`
3. Test burn plan creation: `POST /api/burn-plan`
4. Verify session ID is returned
5. Test error scenarios (invalid config, timeout simulation)

**Automated Integration Tests (Future):**
- Mock AgentCore SDK responses
- Test full request/response flow
- Verify error handling end-to-end

### Property-Based Testing

For this implementation, we're focusing on unit tests for core logic. Property-based testing can be added later for:
- Cost calculation properties
- Retry backoff timing
- UUID generation uniqueness

## API Endpoints

### GET /api/health
**Public endpoint** - No authentication required

**Response:**
```json
{
  "status": "healthy",
  "agentcore_configured": true
}
```

### POST /api/burn-plan
**Public endpoint** - No authentication required (for now)

**Request:**
```json
{
  "config": {
    "amount": "$2500",
    "timeline": 30,
    "stupidity": "Moderately stupid",
    "architecture": "serverless",
    "burning_style": "horizontal"
  }
}
```

**Response (201 Created):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "burn_plan": {
    "total_amount": "$2500",
    "timeline_days": 30,
    "efficiency_level": "Moderately stupid",
    "services_deployed": [...],
    "total_calculated_cost": 2475.50,
    "deployment_scenario": "...",
    "key_mistakes": [...],
    "recommendations": [...]
  }
}
```

**Error Responses:**
- 422: Invalid request data
- 429: Rate limit exceeded (includes Retry-After header)
- 502: Agent error
- 503: AgentCore not configured
- 504: Request timeout

### POST /api/roast
**Public endpoint** - No authentication required (for now)

**Request:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "roast_text": "You spent $2500 on AWS like you're trying to heat the entire cloud..."
}
```

**Error Responses:**
- 404: Session not found
- 429: Rate limit exceeded
- 501: Not implemented (DynamoDB integration pending)
- 502: Agent error
- 504: Request timeout

## Deployment

### Environment Variables

Set these in your deployment environment:
```bash
export AGENTCORE_API_KEY="your-api-key"
export STRANDS_AGENT_ENDPOINT="https://your-endpoint.com"
```

### Deploy Stack

```bash
npm run deploy
```

### Test Endpoints

```bash
# Health check
curl https://your-api.execute-api.region.amazonaws.com/prod/api/health

# Create burn plan
curl -X POST https://your-api.execute-api.region.amazonaws.com/prod/api/burn-plan \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "amount": "$1000",
      "timeline": 30,
      "stupidity": "Mildly dumb",
      "architecture": "serverless",
      "burning_style": "horizontal"
    }
  }'
```

## Future Enhancements

### DynamoDB Integration
- Store burn plans with session IDs
- Enable roast endpoint to retrieve stored sessions
- Add TTL for automatic cleanup

### Cognito Authentication
- Protect burn-plan and roast endpoints
- Associate sessions with user IDs
- Implement user-specific session history

### Monitoring
- CloudWatch metrics for agent invocations
- Error rate tracking
- Latency monitoring
- Cost tracking per user

### Caching
- Cache burn plans for identical configurations
- Reduce agent invocations
- Improve response times
