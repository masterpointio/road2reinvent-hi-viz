"""Test the bill agent and show the complete JSON response."""

import json
from money_spend_aws_bill_agent import invoke

# Test payload
payload = {
    "amount": "$3000",
    "timeline": 30,
    "stupidity": "Very stupid",
    "architecture": "serverless",
    "burning_style": "vertical"
}

print("🔥 Testing Money Spend AWS Bill Agent")
print(f"Payload: {json.dumps(payload, indent=2)}\n")

# Invoke the agent
result = invoke(payload, context=None)

# Print the complete JSON response
print("=" * 80)
print("COMPLETE JSON RESPONSE:")
print("=" * 80)
print(json.dumps(result, indent=2))

# Highlight the PDF URL
if 'pdf_invoice' in result:
    pdf_info = result['pdf_invoice']
    print("\n" + "=" * 80)
    print("📄 PDF INVOICE INFO:")
    print("=" * 80)
    print(f"URL: {pdf_info.get('url')}")
    print(f"Bucket: {pdf_info.get('bucket')}")
    print(f"Key: {pdf_info.get('s3_key')}")
    print(f"Expires in: {pdf_info.get('expiration_seconds')} seconds")
    print(f"Status: {pdf_info.get('upload_status')}")
else:
    print("\n⚠️  No PDF invoice info in response")
