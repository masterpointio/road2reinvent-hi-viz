# Requirements Document

## Introduction

This feature implements a FastAPI Lambda function that acts as a proxy between the frontend and AgentCore backend for the AWS Bill Burner application. The Lambda provides REST API endpoints for generating AWS spending burn plans and roast commentary using Strands agents via the AgentCore SDK. The FastAPI server is bundled using CDK's built-in bundling capabilities with Code.fromAsset, which uses Docker internally to install Python dependencies in a Lambda-compatible environment. The implementation uses the standard aws-lambda.Function construct, providing a scalable backend API that handles multiple endpoints through a single Lambda function (monolithic Lambda pattern).

## Glossary

- **FastAPI Server**: A Python web framework for building APIs with automatic OpenAPI documentation
- **Monolithic Lambda**: A single Lambda function that handles multiple API routes and endpoints
- **API Gateway**: The existing AWS API Gateway REST API that routes HTTP requests to Lambda functions
- **Cognito Authorizer**: The existing authentication mechanism using AWS Cognito User Pools
- **CDK Bundling**: AWS CDK's capability to package Python dependencies by running pip install commands in a Docker container with a Lambda-compatible environment
- **Lambda Proxy Integration**: API Gateway integration pattern that forwards all request details to Lambda
- **Python Runtime**: AWS Lambda execution environment for Python code (Python 3.13)
- **AgentCore SDK**: SDK for invoking Strands agents with structured output capabilities
- **Strands Agent**: AI agent that generates structured responses based on prompts and schemas
- **Burn Plan**: Structured AWS spending scenario with service costs and deployment details
- **Roast Commentary**: Witty commentary about wasteful AWS spending patterns
- **Session**: A stored burn plan identified by a unique session ID

## Requirements

### Requirement 1

**User Story:** As a developer, I want to create a FastAPI Lambda function in the CDK stack, so that I can build a Python-based API with modern framework features.

#### Acceptance Criteria

1. WHEN the CDK stack is synthesized THEN the system SHALL create a Python Lambda function resource with FastAPI dependencies
2. WHEN the Lambda function is deployed THEN the system SHALL use Python 3.13 runtime
3. WHEN bundling the Lambda function THEN the system SHALL include FastAPI and all required dependencies using CDK's native bundling
4. WHEN the Lambda function is invoked THEN the system SHALL initialize the FastAPI application and process requests
5. THE system SHALL NOT require custom Dockerfiles and SHALL use CDK's aws-lambda.Function construct with Code.fromAsset bundling that handles Docker automatically

### Requirement 2

**User Story:** As a developer, I want the FastAPI Lambda to integrate with the existing API Gateway, so that API requests are routed to the FastAPI application.

#### Acceptance Criteria

1. WHEN a request is made to the API Gateway THEN the system SHALL route requests under a specific path prefix to the FastAPI Lambda function
2. WHEN integrating with API Gateway THEN the system SHALL use Lambda proxy integration to forward complete request context
3. WHEN the FastAPI Lambda receives a request THEN the system SHALL parse API Gateway proxy event format and extract HTTP method, path, headers, and body
4. WHEN the FastAPI application processes a request THEN the system SHALL return responses in API Gateway proxy response format
5. WHEN CORS is configured THEN the system SHALL handle preflight OPTIONS requests and include appropriate CORS headers

### Requirement 3

**User Story:** As a developer, I want the FastAPI Lambda to support both public and protected endpoints, so that health checks can be public while future business logic endpoints can use Cognito authentication.

#### Acceptance Criteria

1. WHEN the health check endpoint is configured THEN the system SHALL allow public access without authentication
2. WHEN future protected endpoints are added THEN the system SHALL support attaching the existing Cognito authorizer
3. WHEN an authenticated request is made to a protected endpoint THEN the system SHALL include Cognito user claims in the Lambda event context
4. WHEN the FastAPI application accesses user information THEN the system SHALL extract user identity from the API Gateway request context
5. WHEN an unauthenticated request is made to a protected endpoint THEN the API Gateway SHALL reject the request before invoking the Lambda function

### Requirement 4

**User Story:** As a developer, I want to define a public health check endpoint in the FastAPI application, so that I can verify the API is running and check AgentCore configuration status without authentication.

#### Acceptance Criteria

1. WHEN a GET request is made to /health THEN the system SHALL return a 200 status code with a JSON response containing status information
2. WHEN the health check endpoint is called THEN the system SHALL return a response with a status field indicating "healthy"
3. WHEN the health check endpoint is called THEN the system SHALL return an agentcore_configured field indicating whether AgentCore environment variables are set
4. WHEN the FastAPI application is initialized THEN the system SHALL support adding additional route handlers in the future
5. WHEN the health check is accessed THEN the system SHALL NOT require authentication or authorization

### Requirement 5

**User Story:** As a developer, I want the FastAPI Lambda to handle errors gracefully, so that API consumers receive appropriate error responses.

#### Acceptance Criteria

1. WHEN an unhandled exception occurs in a route handler THEN the system SHALL return a 500 status code with an error message
2. WHEN a route is not found THEN the system SHALL return a 404 status code
3. WHEN the Lambda function fails to initialize THEN the system SHALL log the error and return a 500 status code
4. WHEN errors are logged THEN the system SHALL include request context and stack traces for debugging

### Requirement 6

**User Story:** As a developer, I want the CDK stack to output the FastAPI endpoint URL, so that I can easily access and test the API.

#### Acceptance Criteria

1. WHEN the CDK stack is deployed THEN the system SHALL output the base URL for FastAPI endpoints
2. WHEN the API Gateway URL is constructed THEN the system SHALL include the correct stage and path prefix
3. WHEN viewing stack outputs THEN the system SHALL display the FastAPI endpoint URL in a clearly labeled output

### Requirement 7

**User Story:** As a developer, I want the FastAPI Lambda to have appropriate IAM permissions, so that it can access AWS services if needed in the future.

#### Acceptance Criteria

1. WHEN the Lambda function is created THEN the system SHALL assign an IAM execution role with basic Lambda permissions
2. WHEN the Lambda function needs to log THEN the system SHALL have permissions to write to CloudWatch Logs
3. WHERE additional AWS service access is required THEN the system SHALL allow permissions to be added to the Lambda execution role

### Requirement 8

**User Story:** As a developer, I want to integrate AgentCore SDK with IAM authentication for invoking Strands agents, so that I can generate burn plans and roast commentary using AI agents securely.

#### Acceptance Criteria

1. WHEN the AgentCore client is initialized THEN the system SHALL require AGENTCORE_AGENT_ARN environment variable
2. WHEN the agent ARN is missing THEN the system SHALL raise an AgentCoreError with a descriptive message
3. WHEN the AgentCore client is created THEN the system SHALL configure timeout to 30 seconds and max retries to 2
4. WHEN the AgentCore SDK is not installed THEN the system SHALL raise an AgentCoreError indicating the package is missing
5. WHEN the AgentCore client fails to initialize THEN the system SHALL raise an AgentConnectionError with the underlying error message
6. WHEN the Lambda execution role is configured THEN the system SHALL have permissions to invoke the AgentCore agent via bedrock:InvokeAgent and bedrock:InvokeAgentRuntime actions

### Requirement 9

**User Story:** As a developer, I want to implement retry logic with exponential backoff for AgentCore invocations, so that transient failures are handled gracefully.

#### Acceptance Criteria

1. WHEN an agent invocation times out THEN the system SHALL retry up to 2 times with exponential backoff
2. WHEN a retry is attempted THEN the system SHALL wait 2^attempt seconds before retrying
3. WHEN all retries are exhausted THEN the system SHALL raise the last error encountered
4. WHEN a connection error occurs THEN the system SHALL retry with exponential backoff
5. WHEN a rate limit error occurs THEN the system SHALL NOT retry and SHALL raise AgentRateLimitError immediately

### Requirement 10

**User Story:** As a developer, I want to generate AWS spending burn plans via Strands agents, so that users can see realistic wasteful spending scenarios.

#### Acceptance Criteria

1. WHEN a burn plan is requested THEN the system SHALL accept amount, timeline, stupidity level, architecture type, and burning style parameters
2. WHEN generating a burn plan THEN the system SHALL build instructions that include all configuration parameters
3. WHEN invoking the agent THEN the system SHALL pass structured parameters including amount, timeline, stupidity_level, architecture, and burning_style
4. WHEN the agent returns a response THEN the system SHALL validate it is a dictionary with expected fields
5. WHEN the agent response is valid THEN the system SHALL return a structured burn plan with services and costs

### Requirement 11

**User Story:** As a developer, I want to generate roast commentary via Strands agents, so that users receive witty feedback about their wasteful spending.

#### Acceptance Criteria

1. WHEN roast commentary is requested THEN the system SHALL accept context with total_amount, services, and stupidity_level
2. WHEN generating roast instructions THEN the system SHALL include the total amount and efficiency level
3. WHEN invoking the agent THEN the system SHALL pass parameters including total_amount, services array, and stupidity_level
4. WHEN the agent returns a response THEN the system SHALL extract the roast_text field
5. WHEN roast_text is empty THEN the system SHALL raise an AgentCoreError

### Requirement 12

**User Story:** As a developer, I want comprehensive error handling for AgentCore operations, so that different failure modes return appropriate HTTP status codes.

#### Acceptance Criteria

1. WHEN an agent invocation times out THEN the system SHALL raise AgentTimeoutError
2. WHEN a rate limit is exceeded THEN the system SHALL raise AgentRateLimitError with optional retry_after value
3. WHEN a connection fails THEN the system SHALL raise AgentConnectionError
4. WHEN an invalid response is received THEN the system SHALL raise AgentCoreError
5. WHEN extracting retry-after from error messages THEN the system SHALL parse numeric values using regex

### Requirement 13

**User Story:** As a developer, I want to implement a POST endpoint for burn plan generation, so that users can create new spending scenarios.

#### Acceptance Criteria

1. WHEN a POST request is made to /api/burn-plan THEN the system SHALL accept a BurnPlanRequest with configuration
2. WHEN the request is valid THEN the system SHALL invoke the Strands service to generate a burn plan
3. WHEN the burn plan is generated THEN the system SHALL create a unique session ID using UUID
4. WHEN the burn plan is created THEN the system SHALL return a 201 status code with session ID and burn plan
5. WHEN AgentTimeoutError occurs THEN the system SHALL return 504 Gateway Timeout

### Requirement 14

**User Story:** As a developer, I want to implement a POST endpoint for roast generation, so that users can get commentary about their spending.

#### Acceptance Criteria

1. WHEN a POST request is made to /api/roast THEN the system SHALL accept a RoastRequest with session ID
2. WHEN the session ID is provided THEN the system SHALL retrieve the burn plan from storage
3. WHEN the burn plan is not found THEN the system SHALL return 404 Not Found
4. WHEN the burn plan is found THEN the system SHALL invoke the Strands service to generate roast commentary
5. WHEN roast is generated THEN the system SHALL return a RoastResponse with roast_text

### Requirement 15

**User Story:** As a developer, I want to validate that calculated costs match requested amounts, so that burn plans are realistic and accurate.

#### Acceptance Criteria

1. WHEN a burn plan is generated THEN the system SHALL extract the numeric value from the requested amount string
2. WHEN validating costs THEN the system SHALL calculate 10% tolerance bounds around the requested amount
3. WHEN the calculated cost is outside tolerance bounds THEN the system SHALL raise an AgentCoreError with details
4. WHEN the requested amount cannot be parsed THEN the system SHALL skip validation
5. WHEN the calculated cost is within tolerance THEN the system SHALL accept the burn plan

### Requirement 16

**User Story:** As a developer, I want to define Pydantic models for all API requests and responses, so that data is validated automatically.

#### Acceptance Criteria

1. WHEN defining BurnConfig THEN the system SHALL include fields for amount, timeline, stupidity, architecture, and burning_style
2. WHEN defining ServiceCost THEN the system SHALL include fields for service details, costs, and waste factors
3. WHEN defining BurnPlan THEN the system SHALL include total amount, timeline, services array, and recommendations
4. WHEN defining request models THEN the system SHALL use Field descriptions for API documentation
5. WHEN defining response models THEN the system SHALL include session IDs for tracking

### Requirement 17

**User Story:** As a developer, I want to implement a service layer for Strands agent operations, so that business logic is separated from routing.

#### Acceptance Criteria

1. WHEN the StrandsService is initialized THEN the system SHALL accept an AgentCoreClient instance
2. WHEN generating a burn plan THEN the system SHALL convert BurnConfig to a dictionary for the agent
3. WHEN parsing agent responses THEN the system SHALL validate against the BurnPlan Pydantic model
4. WHEN validation fails THEN the system SHALL raise an AgentCoreError with parsing details
5. WHEN generating roast commentary THEN the system SHALL build context from the burn plan services

### Requirement 18

**User Story:** As a developer, I want to use FastAPI dependency injection for AgentCore client, so that initialization errors are handled consistently.

#### Acceptance Criteria

1. WHEN the get_agentcore_client dependency is called THEN the system SHALL create an AgentCoreClient instance
2. WHEN AgentCoreClient initialization fails THEN the system SHALL raise HTTPException with 503 Service Unavailable
3. WHEN the get_strands_service dependency is called THEN the system SHALL create a StrandsService with the client
4. WHEN dependencies are injected into routes THEN the system SHALL handle initialization errors before route logic
5. WHEN multiple routes use dependencies THEN the system SHALL reuse the same dependency functions
