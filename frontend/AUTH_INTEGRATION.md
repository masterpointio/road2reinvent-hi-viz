# Authentication Integration Guide

## Current State

The authentication infrastructure is ready but uses demo/mock authentication. All routes under `/app` are protected and will redirect unauthenticated users to `/login`.

## Flow

1. **User lands on `/`** → Redirects to `/login`
2. **Login page** → User authenticates (currently demo mode)
3. **After login** → Redirects to `/app` (main landing page)
4. **Main landing** → User clicks "Start Burning" → Goes to `/app/burn-config`
5. **Burn config** → User submits form → Goes to `/app/burn-results`
6. **All API calls** → Include `Authorization: Bearer <token>` header

## Files Structure

```
frontend/src/
├── views/
│   └── LoginView.vue              # Pre-landing login page
├── composables/
│   └── useAuth.ts                 # Auth state management
├── lib/
│   └── apiClient.ts               # API client with auth token support
└── router/
    └── index.ts                   # Route guards
```

## Integration Steps (When Ready)

### 1. Install AWS Amplify or Cognito SDK

```bash
npm install amazon-cognito-identity-js
# or
npm install aws-amplify
```

### 2. Update `useAuth.ts`

Replace the demo login function with actual Cognito authentication:

```typescript
import { CognitoUserPool, AuthenticationDetails, CognitoUser } from 'amazon-cognito-identity-js';

const poolData = {
  UserPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID,
  ClientId: import.meta.env.VITE_COGNITO_CLIENT_ID,
};

const userPool = new CognitoUserPool(poolData);

const login = async (email: string, password: string) => {
  const authenticationData = {
    Username: email,
    Password: password,
  };
  
  const authenticationDetails = new AuthenticationDetails(authenticationData);
  
  const userData = {
    Username: email,
    Pool: userPool,
  };
  
  const cognitoUser = new CognitoUser(userData);
  
  return new Promise((resolve, reject) => {
    cognitoUser.authenticateUser(authenticationDetails, {
      onSuccess: (result) => {
        const token = result.getIdToken().getJwtToken();
        accessToken.value = token;
        user.value = { email, token };
        
        localStorage.setItem('auth_user', JSON.stringify(user.value));
        localStorage.setItem('auth_token', token);
        
        resolve(token);
      },
      onFailure: (err) => {
        reject(err);
      },
    });
  });
};

const logout = () => {
  const cognitoUser = userPool.getCurrentUser();
  if (cognitoUser) {
    cognitoUser.signOut();
  }
  
  user.value = null;
  accessToken.value = null;
  localStorage.removeItem('auth_user');
  localStorage.removeItem('auth_token');
};
```

### 3. Update `LoginView.vue`

Add actual login form with email/password inputs:

```vue
<template>
  <div class="login-form">
    <input v-model="email" type="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <UiButton @click="handleLogin">Sign In</UiButton>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';

const router = useRouter();
const { login } = useAuth();

const email = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
  try {
    await login(email.value, password.value);
    router.push('/app');
  } catch (err) {
    error.value = err.message || 'Login failed';
  }
};
</script>
```

### 4. Environment Variables

Add to `.env`:

```env
VITE_COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
VITE_COGNITO_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXX
VITE_COGNITO_REGION=us-east-1
```

### 5. Backend Integration

The API client (`apiClient.ts`) already includes the auth token in all requests:

```typescript
headers['Authorization'] = `Bearer ${accessToken.value}`;
```

Your backend endpoint should:
1. Validate the JWT token
2. Extract user identity from token
3. Return burn plan data for that user

## Demo Mode

Currently, the app uses demo authentication:
- Any click on "Sign In" will authenticate with a demo token
- Token is stored in localStorage
- All protected routes work as if authenticated
- API calls include the demo token (backend should handle gracefully)

## Testing Auth Flow

1. Clear localStorage: `localStorage.clear()`
2. Navigate to `/` → Should redirect to `/login`
3. Click "Sign In" → Should redirect to `/app`
4. Navigate to `/app/burn-config` → Should work (authenticated)
5. Click logout → Should redirect to `/login`
6. Try to access `/app` directly → Should redirect to `/login`

## Notes

- Route guard checks `isAuthenticated` before allowing access to `/app/*`
- Auth state persists across page refreshes via localStorage
- Token is automatically included in all API requests
- Logout clears all auth state and redirects to login
