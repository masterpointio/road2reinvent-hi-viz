# Implementation Plan: AWS Bill Burner

- [ ] 1. Set up FastAPI application structure and AgentCore SDK integration
  - Create FastAPI application with Mangum adapter for Lambda
  - Set up project structure with routers, services, and utilities
  - Create AgentCore SDK client wrapper utility
  - Configure Strands agent tasks for burn-plan-generator and roast-generator
  - Set up AgentCore SDK authentication and connection handling
  - _Requirements: 3.1, 3.2, 5.1, 5.2, 7.6_

- [ ]* 1.1 Write unit tests for AgentCore SDK client wrapper
  - Test connection handling and error cases
  - Test task invocation with various parameters
  - Test response parsing and validation
  - Test retry logic and timeout handling
  - _Requirements: 3.1, 3.2_

- [ ] 2. Implement DynamoDB burn session storage
  - Create DynamoDB table definition in CDK stack
  - Implement session data model with TTL support
  - Create helper functions for session CRUD operations
  - _Requirements: 3.6, 7.2_

- [ ]* 2.1 Write property test for session storage
  - **Property 10: Total cost matches requested amount**
  - **Validates: Requirements 3.6**

- [ ]* 2.2 Write unit tests for session management
  - Test session creation with valid data
  - Test session retrieval by ID
  - Test TTL expiration handling
  - _Requirements: 7.2_

- [ ] 3. Implement Burn Plan endpoint in FastAPI
  - Create FastAPI router for POST /api/burn-plan
  - Implement Pydantic models for request/response validation
  - Implement Strands agent integration via AgentCore SDK for burn plan generation
  - Implement cost calculation and validation logic
  - Implement session creation and storage
  - Add error handling for all failure scenarios
  - _Requirements: 3.1, 3.2, 3.4, 3.5, 3.6, 7.1_

- [ ]* 3.1 Write property test for burn plan structure
  - **Property 7: Burn plan structure validity**
  - **Validates: Requirements 3.2, 7.1**

- [ ]* 3.2 Write property test for horizontal style
  - **Property 8: Horizontal style produces many resources**
  - **Validates: Requirements 3.4**

- [ ]* 3.3 Write property test for vertical style
  - **Property 9: Vertical style produces fewer expensive resources**
  - **Validates: Requirements 3.5**

- [ ]* 3.4 Write unit tests for burn plan endpoint
  - Test Pydantic model validation (amount, style, stupidity level)
  - Test error responses for invalid inputs
  - Test session ID generation
  - Test FastAPI endpoint routing
  - _Requirements: 2.2, 2.3, 2.4, 7.4_

- [ ] 4. Implement Burn Status endpoint in FastAPI
  - Create FastAPI router for GET /api/burn-status
  - Implement Pydantic models for query parameters and response
  - Implement session lookup from DynamoDB
  - Implement current state calculation based on elapsed time
  - Implement active resources filtering logic
  - Add error handling for missing sessions
  - _Requirements: 7.2, 6.2_

- [ ]* 4.1 Write property test for active resources filtering
  - **Property 13: Resource charts display active resources**
  - **Validates: Requirements 4.3**

- [ ]* 4.2 Write property test for simulation data source
  - **Property 16: Simulation uses plan data not actual resources**
  - **Validates: Requirements 6.2**

- [ ]* 4.3 Write unit tests for burn status endpoint
  - Test status calculation at various time points
  - Test error handling for invalid session IDs
  - Test progress calculation (0.0 to 1.0)
  - Test FastAPI query parameter validation
  - _Requirements: 7.2, 7.4_

- [ ] 5. Implement Roast endpoint in FastAPI
  - Create FastAPI router for POST /api/roast
  - Implement Pydantic models for request/response
  - Implement Strands agent integration via AgentCore SDK for commentary
  - Implement context retrieval from DynamoDB
  - Add error handling and fallback logic
  - _Requirements: 5.1, 5.3, 7.3_

- [ ]* 5.1 Write property test for roast API response
  - **Property 19: Roast API returns commentary**
  - **Validates: Requirements 7.3**

- [ ]* 5.2 Write unit tests for roast endpoint
  - Test roast generation with various spending levels
  - Test error handling for agent failures
  - Test response format validation
  - Test FastAPI request body validation
  - _Requirements: 5.1, 7.3, 7.4_

- [ ] 6. Update CDK stack with all infrastructure
  - Add DynamoDB table for burn sessions
  - Add single FastAPI Lambda function with proper IAM roles
  - Add API Gateway proxy integration for /api/* routes
  - Configure Cognito authorizer for all endpoints
  - Add environment variables for AgentCore SDK and Strands agent configuration
  - Configure CORS via FastAPI middleware
  - _Requirements: 1.1, 7.1, 7.2, 7.3, 7.5, 7.6_

- [ ]* 6.1 Write property test for CORS headers
  - **Property 21: CORS headers present on all responses**
  - **Validates: Requirements 7.5**

- [ ]* 6.2 Write property test for API error codes
  - **Property 20: API errors return appropriate status codes**
  - **Validates: Requirements 7.4**

- [ ] 7. Checkpoint - Ensure backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement frontend configuration form component
  - Create ConfigurationForm.vue with all input fields
  - Implement amount input with validation (positive numbers only)
  - Implement burning style selection (Horizontal/Vertical radio buttons)
  - Implement stupidity level slider (1-10 range)
  - Implement optional time horizon selector
  - Add snarky labels and flavor text throughout
  - Apply neon aesthetic styling to all form elements
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 8.1, 9.3_

- [ ]* 8.1 Write property test for amount validation
  - **Property 3: Amount validation accepts only positive numbers**
  - **Validates: Requirements 2.2**

- [ ]* 8.2 Write property test for burning style validation
  - **Property 4: Burning style validation**
  - **Validates: Requirements 2.3**

- [ ]* 8.3 Write property test for stupidity level validation
  - **Property 5: Stupidity level range validation**
  - **Validates: Requirements 2.4**

- [ ]* 8.4 Write unit tests for configuration form
  - Test form rendering with all fields
  - Test validation error display
  - Test form submission with valid data
  - _Requirements: 2.1, 2.5_

- [ ] 9. Implement frontend API client
  - Create API client service with Axios or Fetch
  - Implement POST /api/burn-plan endpoint call
  - Implement GET /api/burn-status endpoint call
  - Implement POST /api/roast endpoint call
  - Add JWT token handling from Cognito
  - Add error handling and retry logic
  - _Requirements: 2.5, 7.1, 7.2, 7.3_

- [ ]* 9.1 Write property test for configuration submission
  - **Property 6: Configuration submission triggers API call**
  - **Validates: Requirements 2.5**

- [ ]* 9.2 Write unit tests for API client
  - Test all endpoint methods with mocked responses
  - Test error handling for network failures
  - Test JWT token inclusion in headers
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 10. Implement burn visualization components
  - Create BurnVisualization.vue main container
  - Implement simulation timer and state management
  - Implement milestone detection (25%, 50%, 75%, 100%)
  - Implement roast API calls at milestones
  - Add neon-themed layout and styling
  - _Requirements: 4.1, 5.1, 9.1_

- [ ]* 10.1 Write property test for milestone detection
  - **Property 14: Milestones trigger roast generation**
  - **Validates: Requirements 5.1**

- [ ]* 10.2 Write unit tests for burn visualization
  - Test simulation timer initialization
  - Test milestone detection logic
  - Test roast API call triggering
  - _Requirements: 4.1, 5.1_

- [ ] 11. Implement money remaining chart component
  - Create MoneyChart.vue with ECharts integration
  - Implement real-time data updates
  - Implement smooth animations with easing
  - Apply neon glow effects to chart lines
  - Configure chart colors and styling for neon aesthetic
  - _Requirements: 4.2, 4.5, 9.2_

- [ ]* 11.1 Write property test for money decreasing
  - **Property 11: Money remaining decreases monotonically**
  - **Validates: Requirements 4.2**

- [ ]* 11.2 Write property test for simulation completion
  - **Property 12: Simulation ends at zero**
  - **Validates: Requirements 4.5**

- [ ]* 11.3 Write unit tests for money chart
  - Test chart initialization with burn plan data
  - Test data update handling
  - Test final state rendering
  - _Requirements: 4.2, 4.5_

- [ ] 12. Implement resource allocation chart component
  - Create ResourceChart.vue with ECharts integration
  - Implement stacked area or racing bar chart
  - Implement active resource filtering based on time
  - Apply neon styling with glowing effects
  - Add smooth transitions for resource changes
  - _Requirements: 4.3, 9.2_

- [ ]* 12.1 Write unit tests for resource chart
  - Test chart rendering with various resource sets
  - Test active resource filtering
  - Test chart updates over time
  - _Requirements: 4.3_

- [ ] 13. Implement roast commentary display component
  - Create RoastDisplay.vue for commentary
  - Implement chronological ordering of roasts
  - Implement fade-in animations for new comments
  - Apply neon glow effects to text
  - Ensure no overlapping of multiple roasts
  - _Requirements: 5.3, 5.4, 9.1_

- [ ]* 13.1 Write property test for roast ordering
  - **Property 15: Roast commentary displays in order**
  - **Validates: Requirements 5.3, 5.4**

- [ ]* 13.2 Write unit tests for roast display
  - Test rendering of single roast
  - Test rendering of multiple roasts in order
  - Test animation triggering
  - _Requirements: 5.3, 5.4_

- [ ] 14. Implement Cognito authentication flow
  - Update existing LoginView.vue for Bill Burner branding
  - Update CallbackView.vue to handle OAuth flow
  - Implement JWT token storage in Pinia store
  - Implement session expiration handling with redirect
  - Apply neon aesthetic to login UI
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 9.1_

- [ ]* 14.1 Write property test for valid credentials
  - **Property 1: Valid credentials authenticate successfully**
  - **Validates: Requirements 1.2**

- [ ]* 14.2 Write property test for invalid credentials
  - **Property 2: Invalid credentials are rejected**
  - **Validates: Requirements 1.3**

- [ ]* 14.3 Write unit tests for authentication
  - Test login redirect to Cognito
  - Test callback handling with authorization code
  - Test token storage in Pinia
  - Test session expiration redirect
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 15. Implement neon aesthetic styling system
  - Create global CSS variables for neon color palette
  - Implement neon glow effect mixins/utilities
  - Create neon button component styles
  - Create neon input component styles
  - Implement dark background theme
  - Add glowing animation keyframes
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 16. Implement Vue Router configuration
  - Configure routes for login, callback, configuration, and visualization
  - Add route guards for authentication
  - Implement navigation between configuration and visualization
  - Add 404 handling with neon-styled error page
  - _Requirements: 1.1, 2.1, 4.1_

- [ ] 17. Implement Pinia store for application state
  - Create auth store for Cognito tokens and user state
  - Create burn store for burn plan and simulation state
  - Implement actions for API calls
  - Implement getters for computed state
  - Add persistence for auth tokens
  - _Requirements: 1.2, 2.5, 4.2, 5.3_

- [ ] 18. Add frontend error handling and user feedback
  - Implement error boundary components
  - Add toast/notification system for errors
  - Implement loading states for API calls
  - Add retry buttons for failed operations
  - Apply snarky tone to error messages
  - Style all feedback with neon aesthetic
  - _Requirements: 7.4, 8.2_

- [ ]* 18.1 Write unit tests for error handling
  - Test error display for various error types
  - Test retry functionality
  - Test loading state rendering
  - _Requirements: 7.4_

- [ ] 19. Implement AWS pricing validation
  - Create pricing reference data for common AWS services
  - Implement validation logic for burn plan costs
  - Add tolerance checking (±10% for regional variations)
  - _Requirements: 6.3_

- [ ]* 19.1 Write property test for pricing accuracy
  - **Property 17: Displayed costs match AWS pricing**
  - **Validates: Requirements 6.3**

- [ ] 20. Add frontend dependencies and build configuration
  - Install ECharts and vue-echarts
  - Install Vitest and Vue Test Utils
  - Install fast-check for property testing
  - Configure Vite for optimal bundle size
  - Configure TypeScript for strict type checking
  - _Requirements: 4.2, 4.3_

- [ ] 21. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 22. Integration testing and end-to-end validation
  - Test complete flow from configuration to visualization
  - Test authentication flow with real Cognito
  - Test FastAPI endpoints with deployed backend
  - Test API Gateway proxy integration
  - Verify neon aesthetic consistency across all pages
  - Test responsive design on different screen sizes
  - _Requirements: 1.1, 2.1, 4.1, 7.6, 9.1_

- [ ]* 22.1 Write integration tests for user flows
  - Test login → configuration → visualization flow
  - Test error scenarios across the stack
  - Test session expiration handling
  - _Requirements: 1.1, 1.4, 2.1, 4.1_

- [ ] 23. Deploy and configure production environment
  - Deploy CDK stack to AWS with FastAPI Lambda
  - Configure AgentCore SDK credentials and Strands agent endpoint
  - Update frontend environment variables with API Gateway URL
  - Deploy frontend to S3/CloudFront
  - Verify all CloudWatch alarms are configured
  - Test production deployment end-to-end with all FastAPI endpoints
  - _Requirements: All_

- [ ] 24. Final checkpoint - Production validation
  - Ensure all tests pass, ask the user if questions arise.
