# Implementation Plan

- [x] 1. Set up project structure and core interfaces
  - Create directory `lib/lambda/fastapi/` with subdirectories for routers, services, and utils
  - Create `main.py` with Lambda handler using Mangum adapter with `/api` base path
  - Create `app.py` with FastAPI application initialization and CORS middleware
  - Create `requirements.txt` with fastapi, mangum, pydantic, and agentcore dependencies
  - _Requirements: 1.1, 1.3, 1.4_

- [x] 2. Implement Pydantic models for API validation
  - Create `models.py` with all request and response models
  - Define BurnConfig with amount, timeline, stupidity, architecture, and burning_style fields
  - Define ServiceCost with service details, costs, and waste factors
  - Define BurnPlan with complete burn plan structure
  - Define BurnPlanRequest, BurnPlanResponse, RoastRequest, RoastResponse, and HealthResponse
  - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

- [x] 3. Implement AgentCore client wrapper
  - Create `utils/agentcore_client.py` with AgentCoreClient class
  - Implement initialization with environment variable validation
  - Implement custom exception classes: AgentCoreError, AgentTimeoutError, AgentRateLimitError, AgentConnectionError
  - Implement retry logic with exponential backoff (2^attempt seconds)
  - Implement `_invoke_agent` method with timeout and retry handling
  - Implement `_extract_retry_after` helper for parsing rate limit headers
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.1, 9.2, 9.3, 9.4, 9.5, 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 4. Implement burn plan generation in AgentCore client
  - Implement `generate_burn_plan` method in AgentCoreClient
  - Implement `_build_burn_plan_instructions` to create agent prompt
  - Pass structured parameters including amount, timeline, stupidity_level, architecture, and burning_style
  - Validate agent response is a dictionary with expected fields
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 5. Implement roast generation in AgentCore client
  - Implement `generate_roast` method in AgentCoreClient
  - Implement `_build_roast_instructions` to create agent prompt
  - Pass context with total_amount, services array, and stupidity_level
  - Extract and validate roast_text from response
  - Raise AgentCoreError if roast_text is empty
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 6. Implement Strands service layer
  - Create `services/strands_service.py` with StrandsService class
  - Implement `generate_burn_plan` method that converts BurnConfig to dict
  - Implement Pydantic validation for agent responses
  - Implement `_validate_cost_match` to check 10% tolerance
  - Implement `generate_roast` method that builds context from burn plan
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 7. Implement burn plan router with dependency injection
  - Create `routers/burn_plan.py` with APIRouter
  - Implement `get_agentcore_client` dependency function
  - Implement `get_strands_service` dependency function
  - Implement POST endpoint for burn plan creation
  - Generate UUID session ID for each burn plan
  - Handle AgentTimeoutError, AgentRateLimitError, and AgentCoreError with appropriate HTTP status codes
  - Return 201 Created with BurnPlanResponse
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 18.1, 18.2, 18.3, 18.4, 18.5_

- [x] 8. Implement roast router
  - Create `routers/roast.py` with APIRouter
  - Implement POST endpoint for roast generation
  - Return 501 Not Implemented with message about DynamoDB integration
  - Handle AgentTimeoutError, AgentRateLimitError, and AgentCoreError
  - Include Retry-After header for rate limit errors
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [x] 9. Implement health check endpoint
  - Update `app.py` with health check route
  - Check for AGENTCORE_API_KEY and STRANDS_AGENT_ENDPOINT environment variables
  - Return HealthResponse with status and agentcore_configured fields
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 10. Update CDK stack for FastAPI Lambda
  - Add Lambda import to CDK stack file
  - Create Lambda function with Python 3.13 runtime, 29s timeout, 512MB memory
  - Configure Code.fromAsset with bundling for pip install
  - Add AGENTCORE_API_KEY and STRANDS_AGENT_ENDPOINT environment variables
  - _Requirements: 1.2, 1.5, 7.1, 7.2, 7.3_

- [x] 11. Add API Gateway integration
  - Create `/api` resource on existing API Gateway
  - Create `{proxy+}` resource under `/api`
  - Add ANY method with Lambda proxy integration
  - Configure CORS handling
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 12. Add stack output for FastAPI URL
  - Create CfnOutput with FastAPI health check URL
  - Include correct stage and path prefix
  - _Requirements: 6.1, 6.2, 6.3_

- [ ] 13. Deploy and test endpoints
  - Set AGENTCORE_API_KEY and STRANDS_AGENT_ENDPOINT environment variables
  - Run `npm run deploy`
  - Test health endpoint: `GET /api/health`
  - Verify response includes status and agentcore_configured fields
  - Test burn plan creation: `POST /api/burn-plan` with valid config
  - Verify 201 response with session_id and burn_plan
  - Test error scenarios (missing env vars, invalid config)
  - _Requirements: 4.1, 4.2, 4.3, 13.1, 13.4_

- [ ] 14. Verify error handling
  - Test with missing AGENTCORE_API_KEY (should return 503)
  - Test with invalid burn config (should return 422)
  - Verify timeout handling returns 504
  - Verify rate limit handling returns 429 with Retry-After header
  - Verify cost validation rejects plans outside 10% tolerance
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 12.1, 12.2, 12.3, 15.3_
