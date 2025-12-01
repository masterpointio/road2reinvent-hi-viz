"""Money Spend AWS Bill Agent - A Strands agent that analyzes AWS cloud spending and generates PDF invoices.

This agent takes an amount and stupidity level, then reverse-engineers what AWS resources
were likely spun up to result in that spending amount. It generates a professional PDF invoice
and uploads it to S3 with a presigned URL.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

from schema import SpendingAnalysis


DEFAULT_MODEL_ID = os.getenv("MONEY_SPENDER_MODEL", "amazon.nova-lite-v1:0")

# Initialize AgentCore app
app = BedrockAgentCoreApp()


def create_money_spender_agent(
    *,
    model_id: Optional[str] = None,
) -> Agent:
    """Create a Money Spender agent that generates AWS cloud spending plans.

    Args:
        model_id: Bedrock model ID to use (default: amazon.nova-lite-v1:0)

    Returns:
        Configured Strands Agent instance
    """
    system_prompt = (
        "You are an AWS Cloud Cost Forensics Agent. Your job is to reverse-engineer "
        "what over-provisioned and over-engineered AWS resources were likely spun up to result in a given spending amount. "
        "Be creative while staying technically accurate about AWS services and pricing.\n"
        "\n"
        "When given parameters:\n"
        "- Amount spent ($)\n"
        "- Efficiency level (Mildly dumb → Brain damage)\n"
        "\n"
        "Provide a forensic analysis with:\n"
        "1. **Likely Services Used**: Identify combinations of AWS services based on the efficiency level\n"
        "2. **Resource Configurations**: Reverse-engineer the wasteful configurations\n"
        "3. **Cost Breakdown**: Show how the spending occurred across services\n"
        "4. **The Scenario**: Describe what likely happened and why these choices were made\n"
        "\n"
        "EFFICIENCY LEVEL GUIDELINES:\n"
        "\n"
        "**Mildly dumb** - Rookie mistakes and minor over-provisioning:\n"
        "- Over-provisioned EC2 instances (t3.2xlarge for a static website)\n"
        "- Forgot to delete test resources after development\n"
        "- Running RDS databases 24/7 for development environments\n"
        "- Unnecessary data transfer between regions\n"
        "- NAT Gateways left running when not needed\n"
        "- Not using Reserved Instances or Savings Plans\n"
        "\n"
        "**Moderately stupid** - Significant over-provisioning and wasteful patterns:\n"
        "- Multiple redundant databases (RDS, DynamoDB, DocumentDB for the same data)\n"
        "- Expensive instance types for trivial workloads (r7g.16xlarge for a cron job)\n"
        "- Storing logs in S3 Glacier Instant Retrieval then retrieving constantly\n"
        "- Running SageMaker notebooks 24/7 with large ml instances\n"
        "- Using AWS Transfer Family for SFTP when S3 would suffice\n"
        "- Provisioned IOPS on all storage without need\n"
        "- Running CloudFront for internal-only applications\n"
        "\n"
        "**Very stupid** - Extreme over-engineering and architectural disasters:\n"
        "- Multi-region active-active setup for a personal blog\n"
        "- Running EKS with 50 nodes for a single microservice\n"
        "- Using AWS Outposts for a cloud-native application\n"
        "- Managed Blockchain for a simple todo list application\n"
        "- Multiple VPN connections, Direct Connect, and Transit Gateway for a simple app\n"
        "- Running EMR clusters 24/7 with no data processing\n"
        "- Using AWS Wavelength for an internal admin panel\n"
        "- Storing everything in S3 Glacier then using S3 Select constantly\n"
        "- Running AWS Batch with maximum compute for minimal workloads\n"
        "\n"
        "**Brain damage** - Maximum over-engineering with obscure services:\n"
        "- Running AWS RoboMaker simulations continuously\n"
        "- Using AWS Ground Station for basic weather data\n"
        "- Deploying AWS Snowmobile to transfer small amounts of data\n"
        "- Running AWS Thinkbox Deadline render farm for simple presentations\n"
        "- Using Amazon Braket quantum computing for basic calculations\n"
        "- Provisioning AWS Local Zones in every location\n"
        "- Running AWS Elemental MediaLive 24/7 for static content\n"
        "- Using Amazon Monitron IoT sensors for single device monitoring\n"
        "- Deploying AWS Panorama appliances for basic webcam feeds\n"
        "- Running Amazon Nimble Studio for basic image editing\n"
        "- Using AWS Private 5G for a single IoT device\n"
        "- Storing data in every storage class simultaneously\n"
        "- Running AWS DeepRacer for non-ML workloads\n"
        "\n"
        "Include specific instance types, quantities, and realistic AWS pricing. Mix obscure services "
        "with common ones based on the efficiency level. Explain the likely reasoning behind these choices "
        "(over-engineering, lack of cost awareness, misunderstanding requirements, or following tutorials "
        "without understanding the use case).\n"
        "\n"
        "Your response will be structured as JSON with the following schema:\n"
        "- total_amount: STRING - The spending amount provided (e.g., '$1500')\n"
        "- timeline_days: INTEGER - The timeline period in days (e.g., 30, 14, 60)\n"
        "- efficiency_level: STRING - The efficiency level provided\n"
        "- architecture_type: STRING - The architecture type (serverless/kubernetes/traditional/mixed)\n"
        "- burning_style: STRING - The burning style (horizontal/vertical)\n"
        "- services_deployed: ARRAY of objects, each with:\n"
        "  - service_name: STRING - AWS service name (e.g., 'EC2', 'RDS', 'S3')\n"
        "  - instance_type: STRING - Instance type or config (e.g., 'r7g.16xlarge', 'Standard Storage')\n"
        "  - quantity: INTEGER - Number of instances/resources (default 1)\n"
        "  - unit_cost: FLOAT - Cost per unit in dollars\n"
        "  - total_cost: FLOAT - Total cost for this service in dollars\n"
        "  - start_day: INTEGER - Day number when service started (0 = Day 0, 1 = Day 1, etc.)\n"
        "  - end_day: INTEGER - Day number when service stopped (-1 = end of timeline)\n"
        "  - duration_used: STRING - How long the service ran (e.g., '30 days', '15 days', 'entire timeline')\n"
        "  - usage_pattern: STRING - How it's used (e.g., 'Running 24/7', 'Intermittent')\n"
        "  - waste_factor: STRING - Why it's wasteful\n"
        "  - roast: STRING - A brutal, creative one or two-liner roast specifically for THIS service's wasteful usage. "
        "CRITICAL: Each service roast MUST be unique and different. Use varied insults, metaphors, and humor. "
        "Don't repeat the same joke pattern. Examples: 'Using CloudFront for internal apps? That's like hiring a "
        "limo to drive to your bathroom.', 'Running EKS for a single container? Congratulations, you've built a "
        "747 to deliver a pizza.', 'S3 Glacier with constant retrievals? You've invented the world's most expensive "
        "filing cabinet.'\n"
        "- total_calculated_cost: FLOAT - Sum of all service costs in dollars\n"
        "- deployment_scenario: STRING - Detailed narrative of what happened\n"
        "- key_mistakes: ARRAY of STRINGS - 3-5 key mistakes\n"
        "- recommendations: ARRAY of STRINGS - 3-5 recommendations\n"
        "- roast: STRING - A brutal, savage, and absolutely merciless roast of the wasteful spending. "
        "Be creative, funny, and ruthlessly call out the absurdity of these choices. Don't hold back - "
        "this should be a devastating burn that makes the reader question their life choices.\n"
        "\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. The total_calculated_cost MUST EXACTLY match the total_amount provided - this is your PRIMARY goal\n"
        "2. Calculate costs carefully: hourly_rate × 24 hours × days_running × quantity = total_cost\n"
        "3. Adjust service quantities, instance types, and durations to hit the EXACT target amount\n"
        "4. All services_deployed objects MUST have ALL required fields including instance_type, quantity, "
        "start_day (INTEGER), end_day (INTEGER), and duration_used\n"
        "5. Use realistic AWS pricing but scale quantities/durations to match the target amount\n"
        "6. Day numbers must be between 0 and timeline_days, or -1 for end of timeline\n"
        "\n"
        "SCALING EXAMPLES FOR LARGE AMOUNTS:\n"
        "- For $100K+: Use multiple expensive instances (r7g.16xlarge, ml.p4d.24xlarge), high quantities (20-50 instances), "
        "or long durations (entire timeline)\n"
        "- For $500K+: Combine expensive compute (EKS with 100+ nodes), premium databases (db.r6g.16xlarge × 10), "
        "multi-region deployments, and obscure services\n"
        "- For $1M+: Maximum waste - hundreds of instances, most expensive instance types, obscure services running "
        "continuously, multi-region everything, premium support, massive data transfer costs\n"
        "\n"
        "COST CALCULATION TIPS:\n"
        "- EC2 r7g.16xlarge: $3.23/hr × 24 × 30 days × 10 instances = $23,256\n"
        "- SageMaker ml.p4d.24xlarge: $32.77/hr × 24 × 30 days = $23,594 per instance\n"
        "- EKS cluster: $0.10/hr + (node_cost × node_count × hours)\n"
        "- Always verify your math: sum all service costs to ensure they equal the target amount"
    )

    agent = Agent(
        name="money_spend_aws_bill_agent",
        system_prompt=system_prompt,
        model=model_id or DEFAULT_MODEL_ID,
    )

    return agent


def format_spending_analysis(analysis: SpendingAnalysis) -> str:
    """Format the structured analysis into a readable spending report.

    Args:
        analysis: Structured spending analysis from the agent

    Returns:
        Formatted spending analysis string
    """
    header = "=" * 80
    title = "🔍 AWS SPENDING FORENSICS ANALYSIS 🔍"

    # Format services table
    services_output = []
    for service in analysis.services_deployed:
        # Format start and end days
        start_display = f"Day {service.start_day}" if service.start_day > 0 else "Day 0"
        if service.end_day == -1:
            end_display = f"Day {analysis.timeline_days} (end)"
        else:
            end_display = f"Day {service.end_day}"
        
        services_output.append(
            f"\n  📦 {service.service_name}\n"
            f"     Instance/Type: {service.instance_type}\n"
            f"     Quantity: {service.quantity}\n"
            f"     ⏰ Start: {start_display}\n"
            f"     ⏱️  End: {end_display}\n"
            f"     ⏳ Duration: {service.duration_used}\n"
            f"     Unit Cost: ${service.unit_cost:.4f}\n"
            f"     Total Cost: ${service.total_cost:.2f}\n"
            f"     Usage: {service.usage_pattern}\n"
            f"     Waste Factor: {service.waste_factor}\n"
            f"     🔥 Roast: {service.roast}"
        )

    # Format key mistakes
    mistakes_output = "\n".join(f"  ❌ {mistake}" for mistake in analysis.key_mistakes)

    # Format recommendations
    recommendations_output = "\n".join(
        f"  ✅ {rec}" for rec in analysis.recommendations
    )

    # Format roast
    roast_output = f"\n{analysis.roast}\n"

    report = f"""
{header}
{title}
{header}

📊 ANALYSIS PARAMETERS:
  • Amount Spent: {analysis.total_amount}
  • Timeline: {analysis.timeline_days} days
  • Efficiency Level: {analysis.efficiency_level}
  • Architecture Type: {analysis.architecture_type}
  • Burning Style: {analysis.burning_style}
  • Calculated Total: ${analysis.total_calculated_cost:.2f}

{header}

📋 SERVICES DEPLOYED:
{''.join(services_output)}

{header}

📖 DEPLOYMENT SCENARIO:

{analysis.deployment_scenario}

{header}

🚨 KEY MISTAKES:

{mistakes_output}

{header}

💡 RECOMMENDATIONS:

{recommendations_output}

{header}

🔥 THE ROAST 🔥

{roast_output}
{header}
"""
    return report


@app.entrypoint
def invoke(payload: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AgentCore entrypoint for the Money Spender Agent.

    Args:
        payload: Request payload containing:
            - amount: Amount spent (e.g., "$1000")
            - timeline: Timeline in days (e.g., 30)
            - stupidity: Efficiency level (e.g., "Moderately stupid")
            - architecture: Architecture type (e.g., "serverless")
            - burning_style: Burning style (e.g., "horizontal")
        context: AgentCore context

    Returns:
        Dictionary containing the spending analysis
    """
    # Extract parameters from payload
    amount = payload.get("amount", "$1000")
    timeline = payload.get("timeline", 30)
    stupidity = payload.get("stupidity", "Moderately stupid")
    architecture = payload.get("architecture", "mixed")
    burning_style = payload.get("burning_style", "horizontal")
    model_id = payload.get("model_id")

    # Create prompt
    prompt = f"""AWS SPENDING FORENSICS ANALYSIS

💰 TOTAL AMOUNT SPENT: {amount}
📅 TIMELINE: {timeline} days (Day 0 to Day {timeline})
🎯 EFFICIENCY LEVEL: {stupidity}
🏗️ ARCHITECTURE TYPE: {architecture}
🔥 BURNING STYLE: {burning_style}

CRITICAL: You must analyze exactly {amount} in spending over {timeline} days.

Analyze this AWS spending scenario. Based on the "{stupidity}" efficiency level, 
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

Provide a detailed forensic analysis including all required fields."""

    # Create and invoke agent
    agent = create_money_spender_agent(model_id=model_id)
    result = agent(prompt, structured_output_model=SpendingAnalysis)

    # Extract structured output
    analysis = None
    
    if hasattr(result, "structured_output"):
        analysis = result.structured_output
    elif hasattr(result, "data"):
        analysis = result.data
    else:
        # Parse from message content
        message = getattr(result, "message", {})
        content = message.get("content") if isinstance(message, dict) else []
        
        text_content = None
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    text_content = block["text"]
                    break
        
        if text_content:
            # Remove markdown code blocks if present
            text_content = text_content.strip()
            if text_content.startswith("```json"):
                text_content = text_content[7:]
            if text_content.startswith("```"):
                text_content = text_content[3:]
            if text_content.endswith("```"):
                text_content = text_content[:-3]
            
            try:
                data = json.loads(text_content.strip())
                analysis = SpendingAnalysis(**data)
            except (json.JSONDecodeError, Exception):
                analysis = None
    
    # Check if analysis was blocked by content filters
    if analysis is None:
        return {
            "status": "error",
            "error": "content_filtered",
            "message": "The response was blocked by content filters. Try using a less extreme efficiency level (e.g., 'Very stupid' instead of 'Brain damage')."
        }

    # Generate PDF invoice
    from pdf_generator import generate_aws_bill_pdf
    from s3_uploader import upload_pdf_to_s3
    
    pdf_bytes = generate_aws_bill_pdf(analysis)
    
    # Upload to S3 and get presigned URL
    s3_result = upload_pdf_to_s3(pdf_bytes)
    
    # Add PDF info to the analysis
    analysis_dict = analysis.model_dump()
    
    # Build PDF invoice info with error details if upload failed
    pdf_invoice = {
        "url": s3_result.get('s3_url'),
        "s3_key": s3_result.get('s3_key'),
        "bucket": s3_result.get('bucket'),
        "expiration_seconds": s3_result.get('expiration_seconds'),
        "upload_status": s3_result.get('status')
    }
    
    # Add error details if upload failed
    if s3_result.get('status') == 'error':
        pdf_invoice['error_code'] = s3_result.get('error_code')
        pdf_invoice['error_message'] = s3_result.get('error_message')
    
    analysis_dict['pdf_invoice'] = pdf_invoice
    
    # Return the complete analysis directly
    return analysis_dict


if __name__ == "__main__":
    app.run()
