import {
  APIGatewayProxyEvent,
  APIGatewayProxyResult,
  Context,
} from 'aws-lambda';
import {
  BedrockAgentCoreClient,
  InvokeAgentRuntimeCommand,
} from '@aws-sdk/client-bedrock-agentcore';
import { randomUUID } from 'crypto';

interface BurnPlanRequest {
  amount: string | number;
  timeline: number;
  stupidity: string;
  architecture?: string;
  burning_style?: string;
  model_id?: string;
}

interface ServiceCost {
  service_name: string;
  instance_type?: string;
  quantity: number;
  start_day: number;
  end_day: number;
  duration_used: number;
  unit_cost: number;
  total_cost: number;
  usage_pattern?: string;
  waste_factor?: number;
}

interface SpendingAnalysis {
  total_amount: string;
  timeline_days: number;
  efficiency_level: string;
  services_deployed: ServiceCost[];
  total_calculated_cost: number;
  deployment_scenario: string;
  key_mistakes: string[];
  recommendations: string[];
}

const AGENTCORE_AGENT_RUNTIME_ARN =
  process.env.AGENTCORE_AGENT_RUNTIME_ARN || '';
const AWS_REGION = process.env.AWS_REGION || 'us-east-1';

const client = new BedrockAgentCoreClient({ region: AWS_REGION });

export const handler = async (
  event: APIGatewayProxyEvent,
  context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Event:', JSON.stringify(event, null, 2));

  // CORS headers
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };

  // Handle OPTIONS request for CORS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: '',
    };
  }

  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  try {
    // Parse request body
    const body: BurnPlanRequest = JSON.parse(event.body || '{}');

    // Validate required fields
    if (!body.amount || !body.timeline || !body.stupidity) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          error: 'Missing required fields: amount, timeline, stupidity',
        }),
      };
    }

    // Validate AgentCore ARN
    if (!AGENTCORE_AGENT_RUNTIME_ARN) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({
          error: 'AGENTCORE_AGENT_RUNTIME_ARN not configured',
        }),
      };
    }

    // Build instructions for the agent
    const amount = body.amount;
    const timeline = body.timeline;
    const stupidity = body.stupidity;
    const architecture = body.architecture || 'mixed';
    const burningStyle = body.burning_style || 'horizontal';

    const instructions = `AWS SPENDING FORENSICS ANALYSIS

💰 TOTAL AMOUNT SPENT: ${amount}
📅 TIMELINE: ${timeline} days (Day 0 to Day ${timeline})
🎯 EFFICIENCY LEVEL: ${stupidity}
🏗️ ARCHITECTURE TYPE: ${architecture}
🔥 BURNING STYLE: ${burningStyle}

CRITICAL: You must analyze exactly ${amount} in spending over ${timeline} days.

Analyze this AWS spending scenario. Based on the "${stupidity}" efficiency level, 
"${architecture}" architecture type, and "${burningStyle}" burning style, determine what 
over-provisioned and over-engineered AWS resources were likely deployed over the ${timeline} 
day period that would result in EXACTLY ${amount} in total costs.

ARCHITECTURE TYPE REQUIREMENTS:
- **serverless**: Focus on Lambda, API Gateway, DynamoDB, Step Functions, EventBridge, SQS, SNS, AppSync, Cognito
- **kubernetes**: Focus on EKS, ECR, container instances, load balancers, persistent volumes, service mesh
- **traditional**: Focus on EC2, RDS, EBS, ELB, Auto Scaling, VPC components, classic infrastructure
- **mixed**: Combine services from all architecture types in a chaotic over-engineered mess

BURNING STYLE REQUIREMENTS:
- **horizontal**: Spread spending regularly across the entire ${timeline} day timeline. Services run continuously 
  or with consistent patterns. Most services should have start_day=0 and end_day=${timeline} or -1.
- **vertical**: Create burst spending patterns with services spinning up and down at different times. 
  Use varied start_day and end_day values to show one-shot expensive operations or short-lived resources 
  that burn money quickly then shut down.

Provide a detailed forensic analysis including:

1. **Services Deployed**: Identify the AWS services that would result in this spending level. 
   Match the service complexity to the efficiency level provided.

2. **Resource Configurations**: Specify the exact resource types, instance sizes, quantities, 
   storage amounts, and configurations that would generate this cost.

3. **Cost Breakdown**: Show how the ${amount} is distributed across different services over ${timeline} days. 
   Include specific instance types, quantities, start day, end day, duration used, and realistic AWS pricing calculations.
   IMPORTANT: The total_calculated_cost must closely match ${amount} (within 10% variance).

4. **Deployment Scenario**: Describe the likely use case and explain why these particular 
   resources might have been chosen (over-engineering, lack of optimization, following 
   tutorials without adaptation, etc.).

5. **Efficiency Level Interpretation**:
   - Mildly dumb: Minor over-provisioning, forgotten test resources, basic optimization mistakes
   - Moderately stupid: Significant redundancy, expensive instances for simple workloads, poor architecture choices
   - Very stupid: Extreme over-engineering, multi-region for simple apps, massive over-provisioning
   - Brain damage: Maximum over-engineering with obscure/specialized services for basic needs

Include specific AWS service names, instance types, quantities, and realistic pricing. 
Be technically accurate and detailed in your cost calculations.`;

    // Generate unique session ID (must be 33+ characters)
    const sessionId = `${randomUUID()}-${randomUUID().substring(0, 5)}`;

    // Build payload
    const payload = JSON.stringify({
      prompt: instructions,
      amount: body.amount,
      timeline: body.timeline,
      stupidity_level: body.stupidity,
      architecture: architecture,
      burning_style: burningStyle,
    });

    console.log('Invoking AgentCore with session:', sessionId);

    // Invoke AgentCore
    const command = new InvokeAgentRuntimeCommand({
      agentRuntimeArn: AGENTCORE_AGENT_RUNTIME_ARN,
      runtimeSessionId: sessionId,
      payload: payload,
      qualifier: 'DEFAULT',
    });

    const response = await client.send(command);

    // Parse response
    if (!response.response) {
      throw new Error('No response from AgentCore');
    }

    // Read the response stream
    const responseBody = await streamToString(response.response);
    const responseData = JSON.parse(responseBody);

    console.log('AgentCore response:', JSON.stringify(responseData, null, 2));

    // Return success response
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        status: 'success',
        analysis: responseData,
      }),
    };
  } catch (error) {
    console.error('Error:', error);

    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 'error',
      }),
    };
  }
};

// Helper function to convert stream to string
async function streamToString(stream: any): Promise<string> {
  const chunks: Uint8Array[] = [];
  for await (const chunk of stream) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf-8');
}
