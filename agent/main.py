"""Main entry point for the Money Spender Agent.

This script provides a command-line interface to interact with the Money Spender Agent,
allowing users to input an amount and stupidity level to analyze what AWS resources
were likely spun up to result in that spending.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from money_spender_aws_agent import create_money_spender_agent, format_spending_analysis
from schema import SpendingAnalysis


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Money Spender Agent - Analyze AWS cloud spending to determine likely resources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Serverless with horizontal burning
  python main.py --amount "$1000" --timeline 30 --stupidity "Moderately stupid" --architecture serverless --burning-style horizontal

  # Kubernetes with vertical bursts
  python main.py --amount "₹50000" --timeline 14 --stupidity "Brain damage" --architecture kubernetes --burning-style vertical

  # Mixed architecture with regular spending
  python main.py --amount "$500" --timeline 60 --stupidity "Very stupid" --architecture mixed --burning-style horizontal
"""
    )

    parser.add_argument(
        "--amount",
        type=str,
        required=True,
        help="Amount that was spent (e.g., '$1000' or '₹50000')"
    )

    parser.add_argument(
        "--timeline",
        type=int,
        required=True,
        help="Timeline period in days (e.g., 30, 14, 60)"
    )

    parser.add_argument(
        "--stupidity",
        type=str,
        required=True,
        choices=["Mildly dumb", "Moderately stupid", "Very stupid", "Brain damage"],
        help="Efficiency level of resource usage (Mildly dumb → Brain damage)"
    )

    parser.add_argument(
        "--architecture",
        type=str,
        required=True,
        choices=["serverless", "kubernetes", "traditional", "mixed"],
        help="Type of architecture to burn money on (serverless/kubernetes/traditional/mixed)"
    )

    parser.add_argument(
        "--burning-style",
        type=str,
        required=True,
        choices=["horizontal", "vertical"],
        help="Burning style: horizontal (regular spending over timeline) or vertical (one-shot bursts)"
    )

    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Bedrock model ID to use (default: amazon.nova-lite-v1:0)"
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (prompts for inputs)"
    )

    return parser.parse_args()


def interactive_mode():
    """Run the agent in interactive mode."""
    print("=" * 80)
    print("🔍 AWS SPENDING ANALYZER - Interactive Mode 🔍")
    print("=" * 80)
    print()

    try:
        amount = input("How much was spent? (e.g., $1000 or ₹50000): ").strip()
        if not amount:
            print("Error: Amount is required")
            return

        timeline_str = input("Over how many days? (e.g., 30, 14, 60): ").strip()
        if not timeline_str:
            print("Error: Timeline is required")
            return
        
        try:
            timeline = int(timeline_str)
            if timeline <= 0:
                print("Error: Timeline must be a positive number")
                return
        except ValueError:
            print("Error: Timeline must be a number (days)")
            return

        print("\nEfficiency levels (how inefficient was the resource usage?):")
        print("  1. Mildly dumb - Some inefficient choices")
        print("  2. Moderately stupid - Clearly wasteful configurations")
        print("  3. Very stupid - Extremely inefficient setups")
        print("  4. Brain damage - Maximum waste possible")

        choice = input("\nChoose efficiency level (1-4): ").strip()

        stupidity_map = {
            "1": "Mildly dumb",
            "2": "Moderately stupid",
            "3": "Very stupid",
            "4": "Brain damage"
        }

        stupidity = stupidity_map.get(choice)
        if not stupidity:
            print("Error: Invalid choice")
            return

        print("\nArchitecture types:")
        print("  1. Serverless - Lambda, API Gateway, DynamoDB, etc.")
        print("  2. Kubernetes - EKS, containers, orchestration")
        print("  3. Traditional - EC2, RDS, classic infrastructure")
        print("  4. Mixed - Combination of all approaches")

        arch_choice = input("\nChoose architecture type (1-4): ").strip()

        architecture_map = {
            "1": "serverless",
            "2": "kubernetes",
            "3": "traditional",
            "4": "mixed"
        }

        architecture = architecture_map.get(arch_choice)
        if not architecture:
            print("Error: Invalid choice")
            return

        print("\nBurning styles:")
        print("  1. Horizontal - Regular spending spread over timeline")
        print("  2. Vertical - One-shot bursts of spending")

        style_choice = input("\nChoose burning style (1-2): ").strip()

        burning_style_map = {
            "1": "horizontal",
            "2": "vertical"
        }

        burning_style = burning_style_map.get(style_choice)
        if not burning_style:
            print("Error: Invalid choice")
            return

        return amount, timeline, stupidity, architecture, burning_style

    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_prompt(amount: str, timeline: int, stupidity_level: str, architecture: str, burning_style: str) -> str:
    """Create a prompt for the agent based on user inputs.

    Args:
        amount: Amount that was spent
        timeline: Timeline period in days
        stupidity_level: Level of inefficiency in resource usage
        architecture: Type of architecture (serverless/kubernetes/traditional/mixed)
        burning_style: Burning style (horizontal/vertical)

    Returns:
        Formatted prompt string
    """
    prompt = f"""

CRITICAL: You must analyze exactly {amount} in spending over {timeline} days.

Analyze this AWS spending scenario. Based on the "{stupidity_level}" efficiency level, 
"{architecture}" architecture type, and "{burning_style}" burning style, determine what 
over-provisioned and over-engineered AWS resources were likely deployed over the {timeline} 
day period that would result in EXACTLY {amount} in total costs.

ARCHITECTURE TYPE REQUIREMENTS:
- **serverless**: Focus on Lambda, API Gateway, DynamoDB, Step Functions, EventBridge, SQS, SNS, AppSync, Cognito
- **kubernetes**: Focus on EKS, ECR, container instances, load balancers, persistent volumes, service mesh
- **traditional**: Focus on EC2, RDS, EBS, ELB, Auto Scaling, VPC components, classic infrastructure
- **mixed**: Combine services from all architecture types in a chaotic over-engineered mess

BURNING STYLE REQUIREMENTS:
- **horizontal**: Spread spending regularly across the entire {timeline} day timeline. Services run continuously 
  or with consistent patterns. Most services should have start_day=0 and end_day={timeline} or -1.
- **vertical**: Create burst spending patterns with services spinning up and down at different times. 
  Use varied start_day and end_day values to show one-shot expensive operations or short-lived resources 
  that burn money quickly then shut down.

Provide a detailed forensic analysis including:

1. **Services Deployed**: Identify the AWS services that would result in this spending level. 
   Match the service complexity to the efficiency level provided.

2. **Resource Configurations**: Specify the exact resource types, instance sizes, quantities, 
   storage amounts, and configurations that would generate this cost.

3. **Cost Breakdown**: Show how the {amount} is distributed across different services over {timeline} days. 
   Include specific instance types, quantities, start day, end day, duration used, and realistic AWS pricing calculations.
   IMPORTANT: The total_calculated_cost must closely match {amount} (within 10% variance).

4. **Deployment Scenario**: Describe the likely use case and explain why these particular 
   resources might have been chosen (over-engineering, lack of optimization, following 
   tutorials without adaptation, etc.).

5. **Efficiency Level Interpretation**:
   - Mildly dumb: Minor over-provisioning, forgotten test resources, basic optimization mistakes
   - Moderately stupid: Significant redundancy, expensive instances for simple workloads, poor architecture choices
   - Very stupid: Extreme over-engineering, multi-region for simple apps, massive over-provisioning
   - Brain damage: Maximum over-engineering with obscure/specialized services for basic needs

Include specific AWS service names, instance types, quantities, and realistic pricing. 
Be technically accurate and detailed in your cost calculations."""

    return prompt


def main():
    """Main entry point."""
    args = parse_arguments()

    # Interactive mode
    if args.interactive:
        inputs = interactive_mode()
        if not inputs:
            sys.exit(1)
        amount, timeline, stupidity, architecture, burning_style = inputs
    else:
        # Command-line arguments
        amount = args.amount
        timeline = args.timeline
        stupidity = args.stupidity
        architecture = args.architecture
        burning_style = args.burning_style

    # Create the agent
    try:
        agent = create_money_spender_agent(model_id=args.model)
    except Exception as e:
        print(f"❌ Error initializing agent: {e}", file=sys.stderr)
        sys.exit(1)

    # Create prompt
    prompt = create_prompt(amount, timeline, stupidity, architecture, burning_style)

    # Invoke the agent
    try:
        # Invoke agent with structured output model
        result = agent(prompt, structured_output_model=SpendingAnalysis)

        # Extract structured output from result
        # Try different possible attributes
        if hasattr(result, "structured_output"):
            analysis: SpendingAnalysis = result.structured_output
        elif hasattr(result, "data"):
            analysis: SpendingAnalysis = result.data
        else:
            # Parse from message content
            message = getattr(result, "message", {})
            content = message.get("content") if isinstance(message, dict) else []
            
            # Find the text content
            text_content = None
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and "text" in block:
                        text_content = block["text"]
                        break
            
            if text_content:
                # Try to parse JSON from the text
                try:
                    # Remove markdown code blocks if present
                    text_content = text_content.strip()
                    if text_content.startswith("```json"):
                        text_content = text_content[7:]
                    if text_content.startswith("```"):
                        text_content = text_content[3:]
                    if text_content.endswith("```"):
                        text_content = text_content[:-3]
                    
                    data = json.loads(text_content.strip())
                    analysis = SpendingAnalysis(**data)
                except (json.JSONDecodeError, Exception) as e:
                    print(f"❌ Error parsing structured output: {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                print(f"❌ Could not find structured output in result", file=sys.stderr)
                sys.exit(1)

        # Output only JSON
        print(json.dumps(analysis.model_dump(), indent=2))

    except Exception as e:
        print(f"❌ Error generating spending plan: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
