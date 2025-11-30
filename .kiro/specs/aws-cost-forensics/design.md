# Design Document

## Overview

The AWS Cost Forensics Agent is a Python-based system built on the Strands agent framework that performs reverse-engineering analysis of AWS spending. The system takes a spending amount and efficiency level as inputs, then uses an LLM (via Amazon Bedrock) to generate forensic analysis identifying likely AWS resources, configurations, and usage patterns that would result in that spending level.

The design emphasizes simplicity and modularity, with clear separation between agent creation, analysis logic, formatting utilities, and user interfaces.

## Architecture

The system follows a layered architecture:

```
┌─────────────────────────────────────┐
│      User Interface Layer           │
│  (CLI: main.py, Interactive Mode)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Formatting Layer                │
│  (format_spending_analysis)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Agent Layer                    │
│  (Strands Agent Instance)           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      LLM Provider                   │
│  (Amazon Bedrock - Nova Lite)       │
└─────────────────────────────────────┘
```

### Component Responsibilities

1. **User Interface Layer**: Handles command-line arguments, interactive prompts, and output display
2. **Formatting Layer**: Structures raw LLM responses into readable analysis reports
3. **Agent Layer**: Manages Strands agent lifecycle, prompt construction, and LLM invocation
4. **LLM Provider**: Generates forensic analysis based on spending patterns and efficiency levels

## Components and Interfaces

### 1. Agent Module (`money_spender_agent.py`)

**Primary Functions:**

```python
def create_money_spender_agent(
    model_id: str = "amazon.nova-lite-v1:0"
) -> Agent:
    """
    Creates and configures a Strands agent for AWS cost forensics.
    
    Args:
        model_id: Amazon Bedrock model identifier
        
    Returns:
        Configured Strands Agent instance
    """
```

```python
def format_spending_analysis(
    amount: str,
    stupidity_level: str,
    raw_response: str
) -> str:
    """
    Formats raw LLM response into structured analysis.
    
    Args:
        amount: Original spending amount
        stupidity_level: Efficiency level
        raw_response: Raw text from LLM
        
    Returns:
        Formatted analysis string
    """
```

```python
def extract_text(result: Any) -> str:
    """
    Extracts text content from Strands agent result.
    
    Args:
        result: Agent invocation result
        
    Returns:
        Extracted text content
    """
```

**Agent Configuration:**
- Model: Amazon Bedrock Nova Lite (configurable)
- System Prompt: Instructs the LLM to act as an AWS cost forensics expert
- Temperature: 0.7 (balanced creativity and consistency)
- Max Tokens: 2000 (sufficient for detailed analysis)

### 2. Main Interface (`main.py`)

**Command-Line Interface:**

```python
def main():
    """
    Entry point supporting:
    - Flag-based mode: --amount "$5000" --stupidity "Brain damage"
    - Interactive mode: --interactive
    """
```

**Input Validation:**
- Currency parsing ($ and ₹ symbols)
- Stupidity level validation (exact match or fuzzy match)
- Amount range validation ($100 - $1,000,000)

**Output Formatting:**
- Header with input parameters
- Service breakdown section
- Cost analysis section
- Usage patterns section
- Summary footer

### 3. Requirements File (`requirements.txt`)

```
strands-agents>=0.1.0
boto3>=1.26.0
```

## Data Models

### Input Model

```python
@dataclass
class SpendingInput:
    amount: float
    currency: str  # "USD" or "INR"
    stupidity_level: str  # One of the four levels
```

### Analysis Output Model

```python
@dataclass
class ServiceAnalysis:
    service_name: str
    resource_config: str
    cost: float
    percentage: float
    usage_pattern: str

@dataclass
class ForensicAnalysis:
    total_amount: float
    currency: str
    stupidity_level: str
    services: List[ServiceAnalysis]
    overall_pattern: str
```

Note: These models are conceptual. The actual implementation uses string-based formatting for simplicity.

## C
orrectness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Currency parsing correctness
*For any* valid currency string containing $ or ₹ symbols and numeric values, parsing should extract the correct numeric amount and identify the correct currency type (USD or INR).
**Validates: Requirements 1.1**

### Property 2: Stupidity level validation
*For any* input string, validation should accept exactly the four valid stupidity levels ("Mildly dumb", "Moderately stupid", "Very stupid", "Brain damage") and reject all other inputs.
**Validates: Requirements 1.2**

### Property 3: Analysis initiation with valid inputs
*For any* valid spending amount and stupidity level, invoking the agent should produce a non-empty analysis result.
**Validates: Requirements 1.3**

### Property 4: Error handling for invalid inputs
*For any* invalid input (malformed currency, invalid stupidity level, or out-of-range amount), the system should produce an error message or raise an exception rather than proceeding with analysis.
**Validates: Requirements 1.4**

### Property 5: Amount range validation
*For any* spending amount, the system should accept amounts between $100 and $1,000,000 (or equivalent in INR) and reject amounts outside this range.
**Validates: Requirements 1.5**

### Property 6: Minimum service identification
*For any* valid analysis request, the generated output should identify at least 3 distinct AWS services.
**Validates: Requirements 2.1**

### Property 7: Resource specification completeness
*For any* AWS service mentioned in the analysis output (EC2, RDS, S3, or data transfer), the output should include the relevant specification details (instance types for EC2, database engine for RDS, storage class for S3, transfer direction for data transfer).
**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

### Property 8: Cost breakdown structure
*For any* analysis output, each identified service should have an associated cost value, percentage of total, and the costs should be displayed in the same currency as the input.
**Validates: Requirements 4.1, 4.3, 4.5**

### Property 9: Cost sum accuracy
*For any* analysis output, the sum of all individual service costs should equal the input spending amount within 5% tolerance.
**Validates: Requirements 4.2**

### Property 10: Cost ordering
*For any* analysis output with multiple services, the services should be ordered by cost from highest to lowest.
**Validates: Requirements 4.4**

### Property 11: Region specification for global deployments
*For any* analysis output that mentions global or multi-region deployment, the output should include specific AWS region names.
**Validates: Requirements 5.4**

### Property 12: Agent invocation returns results
*For any* valid prompt string, invoking the configured agent should return a structured result object containing analysis text.
**Validates: Requirements 6.2**

### Property 13: Output section structure
*For any* formatted analysis output, the text should contain identifiable sections for services, costs, and usage patterns.
**Validates: Requirements 7.3**

## Error Handling

### Input Validation Errors

1. **Invalid Currency Format**
   - Detection: Regex pattern matching for $ and ₹ symbols with numeric values
   - Response: Raise `ValueError` with message "Invalid currency format. Use $XXXX or ₹XXXX"
   - Recovery: Prompt user for corrected input in interactive mode

2. **Invalid Stupidity Level**
   - Detection: Exact string matching against allowed values
   - Response: Raise `ValueError` with message listing valid options
   - Recovery: Suggest closest match using fuzzy string matching

3. **Out of Range Amount**
   - Detection: Numeric comparison after parsing
   - Response: Raise `ValueError` with message "Amount must be between $100 and $1,000,000"
   - Recovery: Prompt user for corrected input

### Runtime Errors

1. **Bedrock API Errors**
   - Detection: Catch `boto3` exceptions
   - Response: Log error details, display user-friendly message
   - Recovery: Suggest checking AWS credentials and region configuration

2. **LLM Response Parsing Errors**
   - Detection: Validation of response structure
   - Response: Log raw response, return partial results if possible
   - Recovery: Retry with modified prompt or return error to user

3. **Network Errors**
   - Detection: Catch connection exceptions
   - Response: Display connectivity error message
   - Recovery: Suggest checking internet connection and AWS endpoint accessibility

### Error Logging

- All errors logged to stderr with timestamp
- Debug mode available via environment variable `DEBUG=1`
- Structured logging format: `[TIMESTAMP] [LEVEL] [COMPONENT] Message`

## Testing Strategy

The testing strategy employs both unit testing and property-based testing to ensure comprehensive coverage.

### Unit Testing

Unit tests will cover:

1. **Input Parsing Examples**
   - Test parsing "$5000" returns (5000.0, "USD")
   - Test parsing "₹100000" returns (100000.0, "INR")
   - Test parsing "invalid" raises ValueError

2. **Stupidity Level Validation Examples**
   - Test "Brain damage" is accepted
   - Test "brain damage" (lowercase) is accepted with fuzzy matching
   - Test "Invalid Level" is rejected

3. **Agent Creation**
   - Test `create_money_spender_agent()` returns Agent instance
   - Test custom model_id is accepted
   - Test agent has required configuration

4. **Formatting Function**
   - Test `format_spending_analysis()` returns non-empty string
   - Test output contains input parameters
   - Test section headers are present

5. **CLI Interface**
   - Test main.py with valid arguments produces output
   - Test main.py with invalid arguments shows error

### Property-Based Testing

Property-based tests will use the **Hypothesis** library for Python. Each test will run a minimum of 100 iterations with randomly generated inputs.

**Configuration:**
```python
from hypothesis import given, settings
import hypothesis.strategies as st

@settings(max_examples=100)
```

**Test Properties:**

1. **Property 1: Currency parsing correctness**
   - **Feature: aws-cost-forensics, Property 1: Currency parsing correctness**
   - Generator: Random amounts (100-1000000) with $ or ₹ prefix
   - Assertion: Parsed amount matches input, currency type is correct

2. **Property 2: Stupidity level validation**
   - **Feature: aws-cost-forensics, Property 2: Stupidity level validation**
   - Generator: Random strings including valid and invalid levels
   - Assertion: Valid levels accepted, invalid levels rejected

3. **Property 3: Analysis initiation with valid inputs**
   - **Feature: aws-cost-forensics, Property 3: Analysis initiation with valid inputs**
   - Generator: Random valid amounts and stupidity levels
   - Assertion: Agent returns non-empty result

4. **Property 4: Error handling for invalid inputs**
   - **Feature: aws-cost-forensics, Property 4: Error handling for invalid inputs**
   - Generator: Random invalid inputs (malformed strings, out-of-range numbers)
   - Assertion: System raises exception or returns error

5. **Property 5: Amount range validation**
   - **Feature: aws-cost-forensics, Property 5: Amount range validation**
   - Generator: Random amounts including in-range and out-of-range values
   - Assertion: In-range accepted, out-of-range rejected

6. **Property 6: Minimum service identification**
   - **Feature: aws-cost-forensics, Property 6: Minimum service identification**
   - Generator: Random valid analysis requests
   - Assertion: Output contains at least 3 AWS service names

7. **Property 7: Resource specification completeness**
   - **Feature: aws-cost-forensics, Property 7: Resource specification completeness**
   - Generator: Random valid analysis requests
   - Assertion: For each service type mentioned, relevant details are present

8. **Property 8: Cost breakdown structure**
   - **Feature: aws-cost-forensics, Property 8: Cost breakdown structure**
   - Generator: Random valid analysis requests
   - Assertion: Each service has cost, percentage, and correct currency

9. **Property 9: Cost sum accuracy**
   - **Feature: aws-cost-forensics, Property 9: Cost sum accuracy**
   - Generator: Random valid amounts and stupidity levels
   - Assertion: Sum of service costs within 5% of input amount

10. **Property 10: Cost ordering**
    - **Feature: aws-cost-forensics, Property 10: Cost ordering**
    - Generator: Random valid analysis requests
    - Assertion: Service costs appear in descending order

11. **Property 11: Region specification for global deployments**
    - **Feature: aws-cost-forensics, Property 11: Region specification for global deployments**
    - Generator: Random requests with high stupidity levels (likely to trigger global deployment)
    - Assertion: If "global" or "multi-region" mentioned, region names present

12. **Property 12: Agent invocation returns results**
    - **Feature: aws-cost-forensics, Property 12: Agent invocation returns results**
    - Generator: Random valid prompt strings
    - Assertion: Agent returns non-None result with text content

13. **Property 13: Output section structure**
    - **Feature: aws-cost-forensics, Property 13: Output section structure**
    - Generator: Random valid analysis requests
    - Assertion: Output contains section markers for services, costs, patterns

**Test Utilities:**

```python
# Generator for valid currency strings
@st.composite
def currency_string(draw):
    amount = draw(st.floats(min_value=100, max_value=1000000))
    currency = draw(st.sampled_from(['$', '₹']))
    return f"{currency}{amount:.2f}"

# Generator for stupidity levels
stupidity_levels = st.sampled_from([
    "Mildly dumb",
    "Moderately stupid", 
    "Very stupid",
    "Brain damage"
])

# Parser for extracting services and costs from output
def parse_analysis_output(text: str) -> List[Tuple[str, float]]:
    """Extract (service_name, cost) pairs from analysis text"""
    # Implementation uses regex to find service names and associated costs
    pass
```

### Integration Testing

Integration tests will verify end-to-end functionality:

1. **Full Analysis Pipeline**
   - Input: Valid amount and stupidity level
   - Process: Create agent → Invoke → Format → Display
   - Verify: Complete formatted output with all sections

2. **CLI Integration**
   - Execute main.py with various argument combinations
   - Verify exit codes and output format

3. **Error Path Integration**
   - Test complete error handling from input to display
   - Verify error messages reach the user

### Test Execution

```bash
# Run all tests
pytest tests/

# Run only unit tests
pytest tests/unit/

# Run only property-based tests
pytest tests/property/

# Run with coverage
pytest --cov=agent tests/
```

## Implementation Notes

### Prompt Engineering

The system prompt for the agent should:
- Establish the role as an AWS cost forensics expert
- Provide context about stupidity levels and their meanings
- Request structured output format
- Include examples of good analysis
- Emphasize realistic AWS pricing

Example system prompt structure:
```
You are an AWS cost forensics expert who reverse-engineers spending patterns.
Given a spending amount and efficiency level (stupidity level), determine what
AWS resources were likely provisioned.

Stupidity Levels:
- Mildly dumb: Slight over-provisioning
- Moderately stupid: Clear waste with some redundancy
- Very stupid: Extreme inefficiency
- Brain damage: Maximum absurdity, everything over-provisioned

Provide analysis with:
1. At least 3 AWS services
2. Specific resource configurations
3. Cost breakdown per service
4. Usage patterns explaining the scenario

Ensure costs sum to the input amount.
```

### AWS Service Knowledge

The LLM should have knowledge of common AWS services and pricing patterns:
- EC2: Instance types, pricing per hour
- RDS: Database engines, instance classes, storage costs
- S3: Storage classes, request pricing
- Data Transfer: Regional and inter-regional costs
- Lambda: Invocation and duration costs
- CloudFront: Data transfer and request costs
- EBS: Volume types and IOPS pricing

### Extensibility

The design supports future extensions:
- Additional currency support (EUR, GBP, etc.)
- Custom stupidity level definitions
- Integration with actual AWS pricing API
- Historical spending analysis
- Optimization recommendations
- Export to CSV/JSON formats

## Dependencies

### Core Dependencies

```
strands-agents>=0.1.0  # Agent framework
boto3>=1.26.0          # AWS SDK for Bedrock access
```

### Development Dependencies

```
pytest>=7.0.0          # Testing framework
hypothesis>=6.0.0      # Property-based testing
pytest-cov>=4.0.0      # Coverage reporting
black>=22.0.0          # Code formatting
mypy>=0.990            # Type checking
```

### Runtime Requirements

- Python 3.8 or higher
- AWS credentials configured (for Bedrock access)
- Internet connectivity for API calls

## Deployment Considerations

### AWS Configuration

Users must have:
1. AWS credentials configured (`~/.aws/credentials` or environment variables)
2. Bedrock access enabled in their AWS account
3. Appropriate IAM permissions for Bedrock model invocation

### Environment Variables

```bash
AWS_REGION=us-east-1              # Bedrock region
AWS_PROFILE=default               # AWS credential profile
DEBUG=0                           # Enable debug logging
MODEL_ID=amazon.nova-lite-v1:0    # Override default model
```

### Installation

```bash
# Clone repository
git clone <repository-url>
cd aws-cost-forensics

# Install dependencies
pip install -r requirements.txt

# Run
python main.py --amount "$5000" --stupidity "Brain damage"
```
