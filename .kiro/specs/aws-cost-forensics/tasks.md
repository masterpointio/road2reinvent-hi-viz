# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create `agent/` directory in workspace root
  - Create `requirements.txt` with strands-agents and boto3 dependencies
  - Create `agent/__init__.py` for package initialization
  - _Requirements: 6.1, 8.4_

- [x] 2. Implement input validation utilities
  - Create `agent/validation.py` module
  - Implement currency parsing function that extracts amount and currency type from strings with $ and ₹ symbols
  - Implement stupidity level validation function with exact and fuzzy matching
  - Implement amount range validation (100 to 1,000,000)
  - _Requirements: 1.1, 1.2, 1.5_

- [ ]* 2.1 Write property test for currency parsing
  - **Property 1: Currency parsing correctness**
  - **Validates: Requirements 1.1**

- [ ]* 2.2 Write property test for stupidity level validation
  - **Property 2: Stupidity level validation**
  - **Validates: Requirements 1.2**

- [ ]* 2.3 Write property test for amount range validation
  - **Property 5: Amount range validation**
  - **Validates: Requirements 1.5**

- [ ]* 2.4 Write property test for error handling
  - **Property 4: Error handling for invalid inputs**
  - **Validates: Requirements 1.4**

- [x] 3. Implement agent creation and configuration
  - Create `agent/money_spender_agent.py` module
  - Implement `create_money_spender_agent(model_id)` function that returns configured Strands Agent
  - Configure agent with system prompt for AWS cost forensics role
  - Set temperature to 0.7 and max_tokens to 2000
  - Include stupidity level descriptions in system prompt
  - Default model to "amazon.nova-lite-v1:0"
  - _Requirements: 6.1, 6.3, 6.4, 8.5_

- [ ]* 3.1 Write unit test for agent creation
  - Test that `create_money_spender_agent()` returns Agent instance
  - Test that custom model_id parameter is accepted
  - _Requirements: 6.1, 6.3_

- [ ] 4. Implement analysis invocation and result extraction
  - In `agent/money_spender_agent.py`, implement `extract_text(result)` function
  - Function should extract text content from Strands agent result object
  - Handle different result formats gracefully
  - _Requirements: 6.2_

- [ ]* 4.1 Write property test for agent invocation
  - **Property 12: Agent invocation returns results**
  - **Validates: Requirements 6.2**

- [ ]* 4.2 Write property test for analysis initiation
  - **Property 3: Analysis initiation with valid inputs**
  - **Validates: Requirements 1.3**

- [ ] 5. Implement output formatting utilities
  - In `agent/money_spender_agent.py`, implement `format_spending_analysis(amount, stupidity_level, raw_response)` function
  - Format output with header showing input parameters
  - Structure output with clear sections for services, costs, and usage patterns
  - Return formatted string ready for display
  - _Requirements: 6.5, 7.3_

- [ ]* 5.1 Write unit test for formatting function
  - Test that function returns non-empty string
  - Test that output contains input parameters
  - Test that section headers are present
  - _Requirements: 6.5_

- [ ]* 5.2 Write property test for output section structure
  - **Property 13: Output section structure**
  - **Validates: Requirements 7.3**

- [ ] 6. Implement output analysis and validation
  - Create `agent/analysis_parser.py` module
  - Implement function to parse and extract service names from analysis output
  - Implement function to parse and extract costs from analysis output
  - Implement function to validate cost sum against input amount (within 5% tolerance)
  - Implement function to check cost ordering (descending)
  - _Requirements: 2.1, 4.1, 4.2, 4.4_

- [ ]* 6.1 Write property test for minimum service identification
  - **Property 6: Minimum service identification**
  - **Validates: Requirements 2.1**

- [ ]* 6.2 Write property test for cost breakdown structure
  - **Property 8: Cost breakdown structure**
  - **Validates: Requirements 4.1, 4.3, 4.5**

- [ ]* 6.3 Write property test for cost sum accuracy
  - **Property 9: Cost sum accuracy**
  - **Validates: Requirements 4.2**

- [ ]* 6.4 Write property test for cost ordering
  - **Property 10: Cost ordering**
  - **Validates: Requirements 4.4**

- [ ]* 6.5 Write property test for resource specification completeness
  - **Property 7: Resource specification completeness**
  - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**

- [ ]* 6.6 Write property test for region specification
  - **Property 11: Region specification for global deployments**
  - **Validates: Requirements 5.4**

- [ ] 7. Implement command-line interface
  - Create `agent/main.py` as entry point
  - Implement argument parsing for --amount, --stupidity, and --interactive flags
  - Implement flag-based mode that takes amount and stupidity from arguments
  - Implement interactive mode that prompts user for inputs
  - Integrate validation, agent creation, invocation, and formatting
  - Display formatted results to stdout
  - Handle and display errors gracefully
  - _Requirements: 7.1, 7.2, 7.5_

- [ ]* 7.1 Write unit test for CLI with valid arguments
  - Test that main.py with valid arguments produces output
  - Test that main.py with invalid arguments shows error
  - _Requirements: 7.1_

- [ ] 8. Add error handling throughout the system
  - Add try-catch blocks for input validation errors in CLI
  - Add error handling for Bedrock API errors with user-friendly messages
  - Add error handling for network errors
  - Implement logging to stderr with timestamps
  - Add DEBUG environment variable support for verbose logging
  - _Requirements: 1.4_

- [ ] 9. Create documentation and examples
  - Create README.md in agent/ directory with usage instructions
  - Include examples for both CLI modes (flag-based and interactive)
  - Document required AWS configuration and credentials
  - Document environment variables
  - Add example outputs for different stupidity levels
  - _Requirements: 7.1, 7.2_

- [ ] 10. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
