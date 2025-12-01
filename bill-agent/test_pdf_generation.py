"""Test the bill agent PDF generation locally."""

import json
import base64
from money_spend_aws_bill_agent import create_money_spender_agent
from schema import SpendingAnalysis
from pdf_generator import generate_aws_bill_pdf

# Test parameters
amount = "$3000"
timeline = 30
stupidity = "Very stupid"
architecture = "serverless"
burning_style = "vertical"

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

print("🤖 Creating Money Spender Agent...")
agent = create_money_spender_agent()

print("🔍 Analyzing spending...")
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
        raise ValueError("Could not extract structured output from agent response")

print("\n✅ Analysis complete!")
print(f"Total Amount: {analysis.total_amount}")
print(f"Calculated Cost: ${analysis.total_calculated_cost:.2f}")
print(f"Services Deployed: {len(analysis.services_deployed)}")

print("\n📄 Generating PDF invoice...")
pdf_bytes = generate_aws_bill_pdf(analysis)

# Save PDF to file
output_filename = "aws_bill_invoice.pdf"
with open(output_filename, "wb") as f:
    f.write(pdf_bytes)

print(f"✅ PDF saved to: {output_filename}")
print(f"📊 PDF size: {len(pdf_bytes)} bytes")

print("\n🔥 THE ROAST:")
print(analysis.roast)
