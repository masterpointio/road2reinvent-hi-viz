# Money Spender Agent 💸

An AWS spending forensics tool that reverse-engineers what wasteful and over-engineered AWS resources were likely deployed based on a spending amount, timeline, and efficiency level.

## Overview

The Money Spender Agent uses AI to analyze AWS cloud spending patterns and generate detailed forensic reports about what services were likely spun up to result in a given cost. It's perfect for:

- Understanding how AWS costs accumulate
- Learning about AWS services and pricing
- Identifying common cost optimization mistakes
- Creating realistic spending scenarios for training

## Features

- 🔍 **Forensic Analysis**: Reverse-engineer AWS resource deployments from spending amounts
- 📊 **Structured Output**: Get detailed JSON reports with service breakdowns
- ⏱️ **Timeline Tracking**: See when services started and stopped (day-by-day)
- 🎯 **Efficiency Levels**: Four levels from "Mildly dumb" to "Brain damage"
- 💰 **Cost Breakdown**: Detailed per-service cost calculations
- 📝 **Recommendations**: Get suggestions for cost optimization

## Installation

### Prerequisites

- Python 3.8+
- AWS credentials configured (for Bedrock access)
- uv or pip for package management

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd money-spender-agent
```

2. Install dependencies:
```bash
cd agent
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
aws configure
```

## Usage

### Command Line

Basic usage:
```bash
python agent/main.py --amount "$2500" --timeline 30 --stupidity "Moderately stupid"
```

### Parameters

- `--amount`: Amount spent (e.g., "$1000", "₹50000")
- `--timeline`: Timeline in days (e.g., 30, 14, 60)
- `--stupidity`: Efficiency level
  - `"Mildly dumb"`: Minor over-provisioning (10-30% waste)
  - `"Moderately stupid"`: Significant waste (30-60% waste)
  - `"Very stupid"`: Extreme over-engineering (60-85% waste)
  - `"Brain damage"`: Maximum chaos (85-95% waste)
- `--model`: (Optional) Bedrock model ID (default: amazon.nova-lite-v1:0)
- `--interactive`: Run in interactive mode

### Interactive Mode

```bash
python agent/main.py --interactive
```

The interactive mode will prompt you for:
1. Amount spent
2. Timeline in days
3. Efficiency level (1-4)

### Examples

Analyze $5000 over 45 days with high inefficiency:
```bash
python agent/main.py --amount "$5000" --timeline 45 --stupidity "Very stupid"
```

Analyze ₹50000 over 2 weeks with maximum waste:
```bash
python agent/main.py --amount "₹50000" --timeline 14 --stupidity "Brain damage"
```

Use a different model:
```bash
python agent/main.py --amount "$3000" --timeline 30 --stupidity "Moderately stupid" --model "amazon.nova-pro-v1:0"
```

## Output

The agent generates two outputs:

### 1. Console Output

Formatted, human-readable analysis with:
- Analysis parameters (amount, timeline, efficiency level)
- Services deployed with details
- Deployment scenario narrative
- Key mistakes identified
- Recommendations for improvement

### 2. JSON File (`spending_analysis.json`)

Structured data including:
```json
{
  "total_amount": "$2500",
  "timeline_days": 30,
  "efficiency_level": "Moderately stupid",
  "services_deployed": [
    {
      "service_name": "EC2",
      "instance_type": "r7g.16xlarge",
      "quantity": 1,
      "unit_cost": 3.2256,
      "total_cost": 2322.43,
      "start_day": 0,
      "end_day": 30,
      "duration_used": "entire timeline",
      "usage_pattern": "Running 24/7",
      "waste_factor": "Expensive instance type for trivial workload"
    }
  ],
  "total_calculated_cost": 2500.00,
  "deployment_scenario": "...",
  "key_mistakes": [...],
  "recommendations": [...]
}
```

## Efficiency Levels Explained

### Mildly Dumb (10-30% waste)
Rookie mistakes like:
- Over-provisioned instances (t3.2xlarge for static site)
- Forgot to delete test resources
- Running dev databases 24/7
- NAT Gateway left running

### Moderately Stupid (30-60% waste)
Significant over-provisioning:
- Expensive instances for trivial workloads (r7g.16xlarge for cron job)
- Multiple redundant databases
- SageMaker notebooks running 24/7
- CloudFront for internal apps

### Very Stupid (60-85% waste)
Architectural disasters:
- EKS with 50 nodes for single microservice
- Multi-region setup for personal blog
- AWS Outposts for cloud-native app
- Managed Blockchain for todo list

### Brain Damage (85-95% waste)
Maximum chaos with obscure services:
- AWS RoboMaker running 24/7
- Ground Station for weather widget
- Snowmobile to transfer 100GB
- Braket quantum computing for basic math
- Private 5G for single IoT device

## Project Structure

```
.
├── agent/
│   ├── main.py                      # CLI entry point
│   ├── money_spender_aws_agent.py   # Agent implementation
│   ├── schema.py                    # Pydantic schemas
│   └── requirements.txt             # Dependencies
├── .kiro/
│   ├── specs/                       # Feature specifications
│   └── steering/                    # Development guidelines
├── README.md                        # This file
└── spending_analysis.json           # Generated output
```

## Development

### Adding New Features

1. Update schema in `agent/schema.py`
2. Modify system prompt in `agent/money_spender_aws_agent.py`
3. Update CLI in `agent/main.py` if needed
4. Test with various scenarios
5. Update documentation

### Testing

Test with different scenarios:
```bash
# Test all efficiency levels
python agent/main.py --amount "$1000" --timeline 30 --stupidity "Mildly dumb"
python agent/main.py --amount "$2000" --timeline 30 --stupidity "Moderately stupid"
python agent/main.py --amount "$5000" --timeline 30 --stupidity "Very stupid"
python agent/main.py --amount "$10000" --timeline 30 --stupidity "Brain damage"

# Test different timelines
python agent/main.py --amount "$2000" --timeline 7 --stupidity "Moderately stupid"
python agent/main.py --amount "$2000" --timeline 60 --stupidity "Moderately stupid"
python agent/main.py --amount "$2000" --timeline 90 --stupidity "Moderately stupid"
```

## Technologies Used

- **Strands Agents**: AI agent framework
- **Amazon Bedrock**: LLM inference (Nova models)
- **Pydantic**: Data validation and structured output
- **Python 3.8+**: Core language

## Contributing

Contributions are welcome! Please:

1. Follow the coding standards in `.kiro/steering/coding-standards.md`
2. Reference AWS services guide in `.kiro/steering/aws-services-guide.md`
3. Update documentation as needed
4. Test thoroughly before submitting

## License

[Add your license here]

## Acknowledgments

- Built with [Strands Agents](https://strandsagents.com/)
- Powered by Amazon Bedrock
- AWS pricing data from [AWS Pricing Calculator](https://calculator.aws/)

## Support

For issues or questions:
- Check the steering files in `.kiro/steering/`
- Review the specs in `.kiro/specs/aws-cost-forensics/`
- Open an issue on GitHub

---

**Note**: This tool is for educational and analysis purposes. The spending scenarios generated are fictional and based on common AWS cost optimization mistakes.
