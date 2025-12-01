"""AgentCore Runtime handler for Money Spender Agent.

This module provides the AgentCore-compatible entrypoint for deploying
the Money Spender Agent to AWS Bedrock AgentCore Runtime.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

from bedrock_agentcore import BedrockAgentCoreApp
from money_spender_aws_agent import create_money_spender_agent
from schema import SpendingAnalysis

# Initialize AgentCore app
app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AgentCore entrypoint for Money Spender Agent.

    Args:
        payload: Request payload containing:
            - amount: Amount spent (e.g., "$1000")
            - timeline: Timeline in days (e.g., 30)
            - stupidity: Efficiency level (e.g., "Moderately stupid")
            - architecture: Architecture type (e.g., "serverless")
            - burning_style: Burning style (e.g., "horizontal")
            - model_id: Optional Bedrock model ID
        context: AgentCore context object

    Returns:
        Dictionary containing the spending analysis
    """
    try:
        # Extract parameters from payload
        amount = payload.get("amount", "$1000")
        timeline = payload.get("timeline", 30)
        stupidity = payload.get("stupidity", "Moderately stupid")
        architecture = payload.get("architecture", "mixed")
        burning_style = payload.get("burning_style", "horizontal")
        model_id = payload.get("model_id")

        # Validate required parameters
        if not amount or not timeline or not stupidity:
            return {
                "error": "Missing required parameters: amount, timeline, stupidity",
                "status": "error"
            }

        # Create the agent
        agent = create_money_spender_agent(model_id=model_id)

        # Create the prompt
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

        # Invoke the agent
        result = agent(prompt, structured_output_model=SpendingAnalysis)

        # Extract structured output
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
                
                data = json.loads(text_content.strip())
                analysis = SpendingAnalysis(**data)
            else:
                return {
                    "error": "Could not extract structured output from agent response",
                    "status": "error"
                }

        # Return the analysis as a dictionary
        return {
            "status": "success",
            "analysis": analysis.model_dump()
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }


if __name__ == "__main__":
    app.run()
