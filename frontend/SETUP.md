# Frontend Setup Guide

## Environment Configuration

### 1. Copy the environment file
```bash
cp .env.example .env
```

### 2. Configure Cognito (Already Done)
The `.env` file already has:
- `VITE_COGNITO_DOMAIN` - Your Cognito domain
- `VITE_COGNITO_CLIENT_ID` - Your Cognito app client ID

### 3. Add API Base URL
Get the API URL from CDK deployment output:
```bash
cd ..
cdk deploy
# Look for "ApiUrl" in the outputs
```

Then add it to `.env`:
```
VITE_API_BASE_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/
```

### 4. Configure Cognito Callback URLs

In AWS Cognito Console, add these callback URLs to your app client:
- **Localhost**: `http://localhost:5173/login-callback`
- **Production**: `https://yourdomain.com/login-callback`

The app automatically uses the correct callback URL based on the current origin.

## Authentication Flow

1. User visits `/app/*` routes → redirected to `/login` if not authenticated
2. User clicks "Sign in with Cognito" → redirected to Cognito hosted UI
3. After login → redirected to `/login-callback` with authorization code
4. App exchanges code for tokens with Cognito directly
5. Tokens stored in localStorage → user redirected to `/app/dashboard`

## API Integration

The app uses the `useBurnPlan` composable to call the backend:

```typescript
import { useBurnPlan } from '@/composables/useBurnPlan';

const { createBurnPlan, isLoading, error } = useBurnPlan();

const burnPlan = await createBurnPlan({
  totalAmount: 5000,
  timeline: '30d',
  architecture: 'Serverless',
  burningStyle: 'Horizontal',
  efficiencyLevel: 7,
});
```

All API requests automatically include the Cognito access token in the `Authorization` header.

## Development

```bash
npm install
npm run dev
```

Visit `http://localhost:5173`

## Production Build

```bash
npm run build
npm run preview
```
