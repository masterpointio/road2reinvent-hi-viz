# API Setup Guide

## Setting up the API Base URL

The frontend needs to know where your backend API is deployed. Follow these steps:

### 1. Get your API Gateway URL

After deploying the CDK stack, you'll see an output like:

```
Outputs:
R2rStack.ApiEndpoint = https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod
```

### 2. Update your .env file

Open `frontend/.env` and set the `VITE_API_BASE_URL`:

```env
VITE_API_BASE_URL=https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod
```

**Important:** Do NOT include a trailing slash!

### 3. Restart the dev server

If you're running the dev server, restart it to pick up the new environment variable:

```bash
cd frontend
npm run dev
```

## Authentication Flow

The frontend automatically includes the Cognito access token in all API requests:

1. User logs in via Cognito hosted UI
2. Access token is stored in localStorage
3. `apiClient` automatically adds `Authorization: Bearer <token>` header to all requests
4. Backend validates the token via Cognito User Pool

## Testing the Integration

### Check if API URL is configured

Open the browser console and run:

```javascript
console.log(import.meta.env.VITE_API_BASE_URL)
```

### Test the burn plan endpoint

1. Log in to the app
2. Navigate to "Configure Burn"
3. Fill out the form and click "Start Burning"
4. Check the Network tab in DevTools to see the API request

### Common Issues

**401 Unauthorized:**
- Token expired - log out and log back in
- Token not being sent - check browser console for errors

**CORS errors:**
- Backend CORS configuration issue
- Check that the API Gateway has CORS enabled

**Network error:**
- Wrong API URL in .env
- API Gateway not deployed
- VPC/security group blocking requests

**504 Gateway Timeout:**
- Agent is taking too long to respond
- Check AgentCore configuration
- Increase Lambda timeout if needed

## Environment Variables Reference

```env
# Required
VITE_API_BASE_URL=https://your-api-id.execute-api.region.amazonaws.com/prod
VITE_COGNITO_DOMAIN=your-domain.auth.region.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id

# Optional (auto-constructed if not provided)
VITE_COGNITO_LOGIN_URL=https://your-domain.auth.region.amazoncognito.com/login?...
VITE_COGNITO_LOGOUT_URL=https://your-domain.auth.region.amazoncognito.com/logout?...
```
