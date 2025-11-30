# Coding Standards for Money Spender Agent

## Python Style Guide

### General Principles
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

### Code Organization

#### Import Order
1. Standard library imports
2. Third-party imports (strands, pydantic, etc.)
3. Local application imports

```python
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from pydantic import BaseModel, Field
from strands import Agent

from schema import SpendingAnalysis
```

#### Function Structure
```python
def function_name(param: str, optional_param: int = 0) -> ReturnType:
    """Brief description of what the function does.

    Args:
        param: Description of param
        optional_param: Description of optional_param

    Returns:
        Description of return value
    """
    # Implementation
    pass
```

### Pydantic Models

#### Field Definitions
- Always include `Field()` with clear descriptions
- Use appropriate types (str, int, float, List, etc.)
- Set sensible defaults where applicable
- Add validation constraints when needed

```python
class ServiceCost(BaseModel):
    """Cost breakdown for a single AWS service."""

    service_name: str = Field(description="AWS service name (e.g., 'EC2', 'RDS', 'S3')")
    quantity: int = Field(description="Number of instances or resources", default=1)
    total_cost: float = Field(description="Total cost for this service in dollars")
```

### Error Handling

#### CLI Error Handling
- Catch specific exceptions when possible
- Provide helpful error messages to users
- Exit with appropriate status codes (0 for success, 1 for errors)

```python
try:
    result = agent(prompt, structured_output_model=SpendingAnalysis)
    analysis = result.structured_output
except Exception as e:
    print(f"❌ Error generating analysis: {e}")
    sys.exit(1)
```

#### Validation
- Validate user inputs early
- Check for required fields
- Ensure numerical values are in valid ranges

```python
if timeline <= 0:
    print("Error: Timeline must be a positive number")
    return
```

## Strands Agent Best Practices

### System Prompts
- Be explicit about output format requirements
- Include specific examples of AWS services
- Emphasize critical requirements (cost matching, field completeness)
- Structure prompts with clear sections

### Structured Output
- Always use Pydantic models for structured output
- Pass `structured_output_model` parameter during agent invocation
- Access results via `result.structured_output`

```python
agent = Agent(
    name="money_spender_agent",
    system_prompt=system_prompt,
    model=model_id or DEFAULT_MODEL_ID,
)

result = agent(prompt, structured_output_model=SpendingAnalysis)
analysis = result.structured_output
```

## File Naming Conventions

- Use snake_case for Python files: `money_spender_aws_agent.py`
- Use descriptive names that indicate purpose
- Keep module names concise but clear

## Comments and Documentation

### When to Comment
- Complex logic that isn't immediately obvious
- AWS pricing calculations
- Workarounds or non-standard approaches
- TODO items for future improvements

### When NOT to Comment
- Obvious code that explains itself
- Redundant descriptions of what code does

### Docstrings
- Required for all public functions and classes
- Use Google-style docstring format
- Include Args, Returns, and Raises sections as needed

## Testing Considerations

### Manual Testing
- Test with edge cases (very small/large amounts)
- Test all efficiency levels
- Verify JSON output structure
- Check console formatting

### Future Automated Testing
When adding tests:
- Use pytest framework
- Test schema validation
- Test prompt generation
- Mock agent responses for consistency
- Verify cost calculations

## Git Commit Messages

Follow conventional commits format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Examples:
```
feat: add start_day and end_day fields to ServiceCost schema
fix: correct cost calculation for multi-day services
docs: update README with new timeline parameter
refactor: convert timeline input to days
```
