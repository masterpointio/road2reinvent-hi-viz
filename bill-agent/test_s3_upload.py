"""Test the bill agent with S3 upload."""

import json
from money_spend_aws_bill_agent import create_money_spender_agent
from schema import SpendingAnalysis
from pdf_generator import generate_aws_bill_pdf
from s3_uploader import upload_pdf_to_s3, create_bucket_if_not_exists

# Test parameters
amount = "$5000"
timeline = 45
stupidity = "Very stupid"  # Note: "Brain damage" may trigger content filters
architecture = "mixed"
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
print(f"✅ PDF generated ({len(pdf_bytes)} bytes)")

# Create bucket if needed
bucket_name = 'aws-bill-invoices-demo'
print(f"\n🪣 Checking S3 bucket: {bucket_name}")
bucket_exists = create_bucket_if_not_exists(bucket_name)
if bucket_exists:
    print(f"✅ Bucket ready: {bucket_name}")
else:
    print(f"⚠️  Could not create/access bucket: {bucket_name}")
    print("   Using default bucket name from environment")
    bucket_name = None

print("\n☁️  Uploading PDF to S3...")
s3_result = upload_pdf_to_s3(pdf_bytes, bucket_name=bucket_name)

if s3_result['status'] == 'uploaded':
    print("✅ PDF uploaded successfully!")
    print(f"\n📍 S3 Details:")
    print(f"   Bucket: {s3_result['bucket']}")
    print(f"   Key: {s3_result['s3_key']}")
    print(f"   Expiration: {s3_result['expiration_seconds']} seconds")
    print(f"\n🔗 Presigned URL:")
    print(f"   {s3_result['s3_url']}")
    print(f"\n💡 You can download the PDF using the URL above (valid for {s3_result['expiration_seconds']//60} minutes)")
else:
    print(f"❌ Upload failed: {s3_result.get('error_message', 'Unknown error')}")
    if 'error_code' in s3_result:
        print(f"   Error code: {s3_result['error_code']}")

print("\n🔥 THE ROAST:")
print(analysis.roast)
