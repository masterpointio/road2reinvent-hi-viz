# Money Spender Agent - Project Overview

## Purpose
The Money Spender Agent is an AWS spending forensics tool that reverse-engineers what wasteful and over-engineered AWS resources were likely deployed based on a spending amount, timeline, and efficiency level.

## Project Structure

```
.
├── agent/
│   ├── main.py                      # CLI entry point
│   ├── money_spender_aws_agent.py   # Agent implementation
│   ├── schema.py                    # Pydantic schemas for structured output
│   └── requirements.txt             # Python dependencies
├── .kiro/
│   ├── specs/aws-cost-forensics/    # Feature specifications
│   └── steering/                    # Project guidelines (this directory)
└── spending_analysis.json           # Generated output file
```

## Key Components

### 1. Agent (`money_spender_aws_agent.py`)
- Uses Strands Agents framework
- Configured with detailed system prompt about AWS services and pricing
- Returns structured output using Pydantic models
- Supports different efficiency levels: Mildly dumb, Moderately stupid, Very stupid, Brain damage

### 2. CLI (`main.py`)
- Command-line interface with arguments: `--amount`, `--timeline`, `--stupidity`
- Interactive mode available with `--interactive` flag
- Outputs formatted analysis to console and JSON file

### 3. Schema (`schema.py`)
- `ServiceCost`: Individual AWS service cost breakdown
- `SpendingAnalysis`: Complete forensics analysis structure
- All fields are strongly typed for consistency

## Usage Examples

```bash
# Basic usage
python agent/main.py --amount "$2500" --timeline 30 --stupidity "Moderately stupid"

# Interactive mode
python agent/main.py --interactive

# Different efficiency levels
python agent/main.py --amount "$5000" --timeline 45 --stupidity "Very stupid"
python agent/main.py --amount "$1000" --timeline 14 --stupidity "Mildly dumb"
```

## Output Format

The agent generates:
1. **Console output**: Formatted, human-readable analysis
2. **JSON file**: `spending_analysis.json` with structured data

### JSON Schema
- `total_amount`: Spending amount (string)
- `timeline_days`: Timeline in days (integer)
- `efficiency_level`: Efficiency level (string)
- `services_deployed`: Array of services with:
  - `service_name`, `instance_type`, `quantity`
  - `start_day`, `end_day`, `duration_used`
  - `unit_cost`, `total_cost`
  - `usage_pattern`, `waste_factor`
- `total_calculated_cost`: Sum of all costs (float)
- `deployment_scenario`: Narrative description
- `key_mistakes`: List of mistakes
- `recommendations`: List of recommendations

## Development Guidelines

### When Adding New Features
1. Update schema in `schema.py` first
2. Modify system prompt in `money_spender_aws_agent.py`
3. Update CLI arguments in `main.py` if needed
4. Test with various efficiency levels and amounts
5. Update this steering file

### When Modifying Prompts
- Keep AWS service examples realistic and diverse
- Include specific instance types and pricing
- Emphasize matching the target spending amount
- Maintain the efficiency level guidelines

### Testing Checklist
- [ ] Test all four efficiency levels
- [ ] Test various timeline lengths (7, 14, 30, 60, 90 days)
- [ ] Test different spending amounts ($100, $1000, $10000)
- [ ] Verify JSON output is valid
- [ ] Check that calculated cost matches requested amount (within 10%)
- [ ] Ensure start_day and end_day are within timeline bounds
