/**
 * Debug utilities for authentication troubleshooting
 */

import { config } from '../config';

export const debugAuth = () => {
  const info = {
    currentOrigin: window.location.origin,
    callbackUrl: `${window.location.origin}/login-callback`,
    cognitoDomain: config.cognitoDomain,
    cognitoClientId: config.cognitoClientId,
    loginUrl: config.cognitoLoginUrl,
    apiBaseUrl: config.apiBaseUrl,
    hasAccessToken: !!localStorage.getItem('auth_token'),
    hasIdToken: !!localStorage.getItem('id_token'),
  };

  console.group('🔐 Auth Debug Info');
  console.log('Current Origin:', info.currentOrigin);
  console.log('Callback URL:', info.callbackUrl);
  console.log('Cognito Domain:', info.cognitoDomain);
  console.log('Client ID:', info.cognitoClientId);
  console.log('Login URL:', info.loginUrl);
  console.log('API Base URL:', info.apiBaseUrl);
  console.log('Has Access Token:', info.hasAccessToken);
  console.log('Has ID Token:', info.hasIdToken);
  console.groupEnd();

  console.group('📋 Add this to Cognito Callback URLs:');
  console.log(info.callbackUrl);
  console.groupEnd();

  return info;
};

// Make it available globally for easy debugging
if (typeof window !== 'undefined') {
  (window as any).debugAuth = debugAuth;
}
