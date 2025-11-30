import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const claims = event.requestContext.authorizer?.claims;

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    },
    body: JSON.stringify({
      message: 'Hello World!',
      timestamp: new Date().toISOString(),
      user: {
        email: claims?.email || 'unknown',
        sub: claims?.sub || 'unknown',
      },
    }),
  };
};
