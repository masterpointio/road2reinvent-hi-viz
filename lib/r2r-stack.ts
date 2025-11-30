import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda-nodejs';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import * as path from 'path';

export class R2RStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create Cognito User Pool
    const userPool = new cognito.UserPool(this, 'R2RUserPool', {
      userPoolName: 'r2r-user-pool',
      selfSignUpEnabled: true,
      signInAliases: {
        email: true,
      },
      autoVerify: {
        email: true,
      },
      standardAttributes: {
        email: {
          required: true,
          mutable: true,
        },
      },
      passwordPolicy: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
      },
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    // Create User Pool Client
    const userPoolClient = userPool.addClient('R2RUserPoolClient', {
      authFlows: {
        userPassword: true,
        userSrp: true,
      },
      oAuth: {
        flows: {
          authorizationCodeGrant: true,
        },
        scopes: [
          cognito.OAuthScope.EMAIL,
          cognito.OAuthScope.OPENID,
          cognito.OAuthScope.PROFILE,
        ],
        callbackUrls: ['http://localhost:3000/callback'],
        logoutUrls: ['http://localhost:3000/logout'],
      },
    });

    // Create Cognito Domain for Hosted UI
    const userPoolDomain = userPool.addDomain('R2RUserPoolDomain', {
      cognitoDomain: {
        domainPrefix: `r2r-auth-${cdk.Aws.ACCOUNT_ID}`,
      },
    });

    // Create S3 bucket for frontend hosting
    const frontendBucket = new s3.Bucket(this, 'R2RFrontendBucket', {
      bucketName: `r2r-frontend-${cdk.Aws.ACCOUNT_ID}`,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    });

    // Create Route53 Hosted Zone
    const hostedZone = new route53.HostedZone(this, 'R2RHostedZone', {
      zoneName: 'wehavetoomuch.com',
    });

    // Create CloudFront distribution
    const distribution = new cloudfront.Distribution(this, 'R2RDistribution', {
      defaultBehavior: {
        origin: new origins.S3Origin(frontendBucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
      },
      defaultRootObject: 'index.html',
      errorResponses: [
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
        },
        {
          httpStatus: 403,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
        },
      ],
    });

    // Create A Record for CloudFront distribution
    new route53.ARecord(this, 'R2RARecord', {
      zone: hostedZone,
      recordName: 'wehavetoomuch.com',
      target: route53.RecordTarget.fromAlias(
        new targets.CloudFrontTarget(distribution)
      ),
    });

    // Update User Pool Client with CloudFront URLs
    const cloudFrontUrl = `https://${distribution.distributionDomainName}`;
    const userPoolClientCfn = userPoolClient.node
      .defaultChild as cognito.CfnUserPoolClient;
    userPoolClientCfn.callbackUrLs = [
      'http://localhost:5173/callback',
      `${cloudFrontUrl}/callback`,
    ];
    userPoolClientCfn.logoutUrLs = [
      'http://localhost:5173/logout',
      `${cloudFrontUrl}/logout`,
    ];

    // Create Lambda function
    const helloWorldFunction = new lambda.NodejsFunction(this, 'HelloWorldFunction', {
      functionName: 'hello-world',
      entry: path.join(__dirname, 'lambda', 'hello-world.ts'),
      handler: 'handler',
      runtime: cdk.aws_lambda.Runtime.NODEJS_20_X,
      bundling: {
        externalModules: ['aws-sdk'],
      },
    });

    // Create API Gateway with Cognito Authorizer
    const api = new apigateway.RestApi(this, 'R2RApi', {
      restApiName: 'r2r-api',
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: ['Content-Type', 'Authorization'],
      },
    });

    const cognitoAuthorizer = new apigateway.CognitoUserPoolsAuthorizer(
      this,
      'CognitoAuthorizer',
      {
        cognitoUserPools: [userPool],
      }
    );

    const helloResource = api.root.addResource('hello');
    helloResource.addMethod('GET', new apigateway.LambdaIntegration(helloWorldFunction), {
      authorizer: cognitoAuthorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
    });

    // Deploy frontend to S3
    new s3deploy.BucketDeployment(this, 'R2RFrontendDeployment', {
      sources: [s3deploy.Source.asset('./frontend/dist')],
      destinationBucket: frontendBucket,
      distribution,
      distributionPaths: ['/*'],
    });

    // Output the Hosted UI URL
    new cdk.CfnOutput(this, 'UserPoolId', {
      value: userPool.userPoolId,
      description: 'Cognito User Pool ID',
    });

    new cdk.CfnOutput(this, 'UserPoolClientId', {
      value: userPoolClient.userPoolClientId,
      description: 'Cognito User Pool Client ID',
    });

    new cdk.CfnOutput(this, 'CognitoDomain', {
      value: `${userPoolDomain.domainName}.auth.${cdk.Aws.REGION}.amazoncognito.com`,
      description: 'Cognito Domain',
    });

    new cdk.CfnOutput(this, 'HostedUIUrl', {
      value: `https://${userPoolDomain.domainName}.auth.${cdk.Aws.REGION}.amazoncognito.com/login?client_id=${userPoolClient.userPoolClientId}&response_type=code&redirect_uri=${cloudFrontUrl}/callback`,
      description: 'Cognito Hosted UI Login URL',
    });

    new cdk.CfnOutput(this, 'CloudFrontUrl', {
      value: `https://${distribution.distributionDomainName}`,
      description: 'CloudFront Distribution URL',
    });

    new cdk.CfnOutput(this, 'FrontendBucketName', {
      value: frontendBucket.bucketName,
      description: 'Frontend S3 Bucket Name',
    });

    new cdk.CfnOutput(this, 'ApiUrl', {
      value: api.url,
      description: 'API Gateway URL',
    });

    new cdk.CfnOutput(this, 'HostedZoneId', {
      value: hostedZone.hostedZoneId,
      description: 'Route53 Hosted Zone ID',
    });

    new cdk.CfnOutput(this, 'NameServers', {
      value: cdk.Fn.join(', ', hostedZone.hostedZoneNameServers || []),
      description: 'Route53 Name Servers',
    });
  }
}
