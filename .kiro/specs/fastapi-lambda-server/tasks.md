# Implementation Plan

- [x] 1. Create Python Lambda function structure

  - Create directory `lib/lambda/fastapi/`
  - Create `main.py` with Lambda handler using Mangum adapter with `/api` base path
  - Create `app.py` with FastAPI application and `/health` endpoint
  - Create `requirements.txt` with fastapi and mangum dependencies
  - _Requirements: 1.1, 1.3, 1.4, 4.1, 4.2_

- [ ] 2. Update CDK stack to add FastAPI Lambda

  - Add Lambda import statement to stack file
  - Create Lambda function with Python 3.13 runtime, 29s timeout, 512MB memory
  - Configure Code.fromAsset with bundling for pip install
  - _Requirements: 1.2, 1.5_

- [ ] 3. Add API Gateway integration

  - Create `/api` resource on existing API Gateway
  - Create `{proxy+}` resource under `/api`
  - Add ANY method with Lambda proxy integration
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 4. Add stack output for FastAPI URL

  - Create CfnOutput with FastAPI health check URL
  - _Requirements: 6.1, 6.2, 6.3_

- [ ] 5. Deploy and verify
  - Run `npm run deploy`
  - Test health endpoint with curl
  - Verify response is `{"status": "healthy"}`
  - _Requirements: 4.1, 4.2_
