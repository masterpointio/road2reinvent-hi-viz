"""Invoke the Money Spend AWS Bill Agent via AgentCore Runtime."""

import json
import boto3
import base64

# Initialize the AgentCore client
client = boto3.client('bedrock-agentcore', region_name='us-east-1')

# Prepare the payload for the Money Spend AWS Bill Agent
# Note: "Brain damage" level may trigger content filters, use "Very stupid" instead
payload = json.dumps({
    "amount": "$1000000",
    "timeline": 45,
    "stupidity": "Moderately stupid",
    "architecture": "mixed",
    "burning_style": "vertical"
})

print("🔥 Invoking Money Spend AWS Bill Agent via AgentCore Runtime...")
print(f"Payload: {payload}\n")

try:
    # Invoke the agent (using the existing money_spender_aws_agent)
    # Note: The bill-agent needs to be deployed separately to have its own ARN
    response = client.invoke_agent_runtime(
        agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:114713347049:runtime/money_spend_aws_bill_agent-4UONHCBVbf',
        runtimeSessionId='bill-agent-session-12345678901234567890',  # Must be 33+ chars
        payload=payload,
        qualifier="DEFAULT"  # Optional
    )
    
    # Read and parse the response
    response_body = response['response'].read()
    response_data = json.loads(response_body)
    print(response_data)
    print("=" * 80)
    print("Agent Response:")
    print("=" * 80)
    
    # Check if response is an error
    if response_data.get('status') == 'error':
        print(f"\n❌ ERROR: {response_data.get('error')}")
        print(f"Message: {response_data.get('message')}")
    else:
        # Response contains the analysis directly
        print(f"\n📊 SPENDING ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"Total Amount: {response_data['total_amount']}")
        print(f"Timeline: {response_data['timeline_days']} days")
        print(f"Efficiency Level: {response_data['efficiency_level']}")
        print(f"Architecture: {response_data['architecture_type']}")
        print(f"Burning Style: {response_data['burning_style']}")
        print(f"Calculated Cost: ${response_data['total_calculated_cost']:.2f}")
        print(f"Services Deployed: {len(response_data['services_deployed'])}")
        
        print("\n🔥 THE ROAST 🔥")
        print(response_data['roast'])
        
        # Check for PDF invoice info
        if 'pdf_invoice' in response_data:
            pdf_info = response_data['pdf_invoice']
            print("\n" + "=" * 80)
            print("📄 PDF INVOICE")
            print("=" * 80)
            
            upload_status = pdf_info.get('upload_status', 'unknown')
            print(f"Upload Status: {upload_status}")
            
            if upload_status == 'uploaded':
                expiration = pdf_info.get('expiration_seconds', 0) or 0
                print(f"S3 Bucket: {pdf_info.get('bucket', 'N/A')}")
                print(f"S3 Key: {pdf_info.get('s3_key', 'N/A')}")
                print(f"URL Expiration: {expiration} seconds ({expiration//3600} hours)")
                print(f"\n🔗 Download PDF:")
                print(f"{pdf_info.get('url', 'N/A')}")
            else:
                print(f"❌ PDF Upload Failed")
                error_code = pdf_info.get('error_code', 'N/A')
                error_msg = pdf_info.get('error_message', 'Unknown error')
                print(f"Error Code: {error_code}")
                print(f"Error Message: {error_msg}")
                print(f"S3 Bucket: {pdf_info.get('bucket', 'N/A')}")
                print(f"S3 Key: {pdf_info.get('s3_key', 'N/A')}")
        else:
            print("\n⚠️  No PDF invoice info in response")
    
    # Print full response for debugging
    print("\n" + "=" * 80)
    print("Full Response (JSON):")
    print("=" * 80)
    print(json.dumps(response_data, indent=2))

except Exception as e:
    print(f"❌ Error invoking agent: {e}")
    import traceback
    traceback.print_exc()
