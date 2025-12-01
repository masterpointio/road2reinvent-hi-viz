"""Invoke the Money Spender Agent via AgentCore Runtime."""

import json
import boto3

# Initialize the AgentCore client
client = boto3.client('bedrock-agentcore', region_name='us-east-1')

# Prepare the payload for the Money Spender Agent
payload = json.dumps({
    "amount": "$3000",
    "timeline": 30,
    "stupidity": "Very stupid",
    "architecture": "serverless",
    "burning_style": "vertical"
})

print("Invoking Money Spender Agent via AgentCore Runtime...")
print(f"Payload: {payload}\n")

try:
    # Invoke the agent
    response = client.invoke_agent_runtime(
        agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:114713347049:runtime/money_spender_aws_agent-VDHCzRHLoE',
        runtimeSessionId='money-spender-session-12345678901234567890',  # Must be 33+ chars
        payload=payload,
        qualifier="DEFAULT"  # Optional
    )
    
    # Read and parse the response
    response_body = response['response'].read()
    response_data = json.loads(response_body)
    
    print("=" * 80)
    print("Agent Response:")
    print("=" * 80)
    print(json.dumps(response_data, indent=2))
    
    # If the response contains the analysis, pretty print it
    if 'analysis' in response_data:
        analysis = response_data['analysis']
        print("\n" + "=" * 80)
        print("SPENDING ANALYSIS SUMMARY")
        print("=" * 80)
        print(f"Total Amount: {analysis['total_amount']}")
        print(f"Timeline: {analysis['timeline_days']} days")
        print(f"Efficiency Level: {analysis['efficiency_level']}")
        print(f"Architecture: {analysis['architecture_type']}")
        print(f"Burning Style: {analysis['burning_style']}")
        print(f"Calculated Cost: ${analysis['total_calculated_cost']:.2f}")
        print(f"\nServices Deployed: {len(analysis['services_deployed'])}")
        
        print("\n🔥 THE ROAST 🔥")
        print(analysis['roast'])

except Exception as e:
    print(f"❌ Error invoking agent: {e}")
    import traceback
    traceback.print_exc()
