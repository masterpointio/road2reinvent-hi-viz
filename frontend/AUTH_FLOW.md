# Authentication Flow Implementation

## What Was Set Up

### 1. Route Protection
- All `/app/*` routes now require authentication (`meta: { requiresAuth: true }`)
- Unauthenticated users are redirected to `/login`
- Router guard checks authentication status before each navigation

### 2. Dynamic Callback URLs
The app now automatically uses the correct callback URL based on the current environment:
- **Localhost**: `http://localhost:5173/login-callback`
- **Production**: `https://yourdomain.com/login-callback`

No hardcoded URLs in the config - it uses `window.location.origin` dynamically.

### 3. Token Exchange
The `useAuth` composable now handles the full OAuth2 flow:
1. User clicks login → redirected to Cognito hosted UI
2. Cognito redirects back with authorization code
3. App exchanges code for tokens directly with Cognito (no backend needed)
4. Tokens stored in localStorage
5. User redirected to dashboard

### 4. API Integration with Auth
Created `useBurnPlan` composable that:
- Calls `/burn-plan` endpoint with authenticated requests
- Automatically includes Cognito access token in headers
- Transforms backend response to frontend format
- Handles loading states and errors

### 5. Updated BurnConfigurationView
- Now calls real API instead of mock data
- Uses `createBurnPlan()` from `useBurnPlan` composable
- Shows loading state while generating plan
- Displays error messages on failure

## Configuration Required

### In AWS Cognito Console
Add these callback URLs to your app client settings:
- `http://localhost:5173/login-callback` (for local dev)
- `https://yourdomain.com/login-callback` (for production)

### In `.env` File
```bash
# Required
VITE_COGNITO_DOMAIN=r2r-auth-114713347049.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=69fd6e78jd23pctos94qbq4uqr

# Get from CDK output
VITE_API_BASE_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/
```

## Files Modified

1. **frontend/src/router/index.ts** - Added route protection
2. **frontend/src/config.ts** - Dynamic callback URL generation
3. **frontend/src/composables/useAuth.ts** - Direct Cognito token exchange
4. **frontend/src/composables/useBurnPlan.ts** - NEW: API integration
5. **frontend/src/views/BurnConfigurationView.vue** - Real API calls
6. **frontend/.env.example** - Updated documentation
7. **frontend/env.d.ts** - Added type definitions

## Testing the Flow

1. Start the dev server: `npm run dev`
2. Visit `http://localhost:5173/app/dashboard`
3. Should redirect to `/login`
4. Click "Sign in with Cognito"
5. Login with Cognito credentials
6. Should redirect back and exchange token
7. Should land on `/app/dashboard` authenticated
8. Try creating a burn plan - should call real API with auth token

## API Request Format

When calling `/burn-plan`, the request looks like:
```json
{
  "config": {
    "total_amount": 5000,
    "timeline": "30d",
    "architecture": "Serverless",
    "burning_style": "Horizontal",
    "efficiency_level": 7
  }
}
```

Headers include:
```
Authorization: Bearer <cognito-access-token>
Content-Type: application/json
```
