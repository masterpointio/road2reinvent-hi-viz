# Cognito Authentication Implementation

## ✅ What's Been Implemented

### 1. **useAuth Composable** (`src/composables/useAuth.ts`)
- Full Cognito OAuth 2.0 authorization code flow
- Token exchange with Cognito token endpoint
- ID token decoding to extract user information
- Secure token storage in localStorage
- Support for both implicit flow (tokens in URL) and authorization code flow

### 2. **Login Flow** (`src/views/LoginView.vue`)
- Redirects to Cognito Hosted UI for authentication
- Detects if Cognito is configured
- Sign-up link redirects to Cognito sign-up page

### 3. **Callback Handler** (`src/views/LoginCallbackView.vue`)
- Handles OAuth callback from Cognito
- Exchanges authorization code for tokens
- Extracts and stores access token and ID token
- Redirects to `/app` after successful authentication

### 4. **Logout Flow** (`src/layouts/AppLayout.vue`)
- Clears local auth state
- Redirects to Cognito logout endpoint
- Cognito redirects back to `/login` after logout

### 5. **Route Guards** (`src/router/index.ts`)
- Already configured to protect `/app/*` routes
- Redirects unauthenticated users to `/login`

### 6. **API Client** (`src/lib/apiClient.ts`)
- Already configured to include `Authorization: Bearer <token>` header
- Uses `accessToken` from useAuth composable

## 🔧 Configuration Required

Set these environment variables in `.env`:

```env
VITE_COGNITO_DOMAIN=your-domain.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-client-id
VITE_API_BASE_URL=https://your-api.execute-api.us-east-1.amazonaws.com
```

## 🔄 Authentication Flow

### Login Flow:
1. User visits `/` → redirects to `/login`
2. User clicks "Sign In" → redirects to Cognito Hosted UI
3. User authenticates with Cognito
4. Cognito redirects to `/login-callback?code=...`
5. Callback handler exchanges code for tokens
6. Tokens stored in localStorage
7. User redirected to `/app`

### API Request Flow:
1. User makes API request (e.g., create burn plan)
2. API client automatically includes `Authorization: Bearer <access_token>`
3. Backend validates JWT token
4. Backend returns data for authenticated user

### Logout Flow:
1. User clicks logout in nav menu
2. Local auth state cleared
3. Redirect to Cognito logout URL
4. Cognito clears session and redirects to `/login`

## 📝 Token Storage

Tokens are stored in localStorage:
- `auth_access_token`: Access token for API requests
- `auth_id_token`: ID token with user claims
- `auth_user`: User object with email

## 🔐 Security Features

- ✅ Authorization code flow (more secure than implicit flow)
- ✅ Tokens stored in localStorage (consider httpOnly cookies for production)
- ✅ Automatic token inclusion in API requests
- ✅ Route guards prevent unauthorized access
- ✅ Proper logout clears all auth state

## 🧪 Testing

### With Cognito Configured:
1. Start dev server: `npm run dev`
2. Visit `http://localhost:5173`
3. Should redirect to `/login`
4. Click "Sign In" → redirects to Cognito
5. Sign in with Cognito credentials
6. Should redirect back and land on `/app`
7. Make API requests → tokens automatically included
8. Click logout → clears session and redirects to login

### Without Cognito (Demo Mode):
- Shows warning message about missing configuration
- Can still test UI without backend

## 🚀 Next Steps

1. **Set environment variables** with your Cognito configuration
2. **Test the full flow** from login to API requests
3. **Configure Cognito User Pool** with correct callback URLs:
   - Callback URL: `http://localhost:5173/login-callback` (dev)
   - Callback URL: `https://your-domain.com/login-callback` (prod)
   - Sign out URL: `http://localhost:5173/login` (dev)
   - Sign out URL: `https://your-domain.com/login` (prod)

## 📚 Key Files

- `src/composables/useAuth.ts` - Auth state and logic
- `src/views/LoginView.vue` - Login page
- `src/views/LoginCallbackView.vue` - OAuth callback handler
- `src/lib/apiClient.ts` - API client with auth headers
- `src/router/index.ts` - Route guards
- `src/config.ts` - Cognito configuration
- `frontend/AUTH_INTEGRATION.md` - Original integration guide

## 💡 Tips

- Check browser console for auth errors
- Verify Cognito callback URLs match exactly
- Access token is used for API authorization
- ID token contains user information (email, sub, etc.)
- Tokens expire - implement refresh token flow if needed
