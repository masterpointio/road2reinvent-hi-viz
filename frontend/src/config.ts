/**
 * Centralized configuration for the application
 * All environment variables are accessed here for easy management
 */

const getRedirectUri = (): string => {
  return `${window.location.origin}/login-callback`;
};

const getCognitoLoginUrl = (): string => {
  const domain = import.meta.env.VITE_COGNITO_DOMAIN;
  const clientId = import.meta.env.VITE_COGNITO_CLIENT_ID;
  
  if (!domain || !clientId) {
    return '';
  }

  const redirectUri = getRedirectUri();
  return `https://${domain}/login?client_id=${clientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}`;
};

export const config = {
  // Application
  appName: 'Bill Burner',

  // API Configuration
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || '',

  // Cognito Configuration
  cognitoDomain: import.meta.env.VITE_COGNITO_DOMAIN || '',
  cognitoClientId: import.meta.env.VITE_COGNITO_CLIENT_ID || '',
  cognitoLoginUrl: import.meta.env.VITE_COGNITO_LOGIN_URL || getCognitoLoginUrl(),
  cognitoLogoutUrl: import.meta.env.VITE_COGNITO_LOGOUT_URL || '',

  // Feature Flags (for quick toggles during hackathon)
  features: {
    enableToasts: true,
    enableThemeSwitcher: true,
  },
} as const;

/**
 * Helper to get the Cognito logout URL
 * Constructs it from domain and client ID if not explicitly set
 */
export const getCognitoLogoutUrl = (): string => {
  if (config.cognitoLogoutUrl) {
    return config.cognitoLogoutUrl;
  }

  if (config.cognitoDomain && config.cognitoClientId) {
    const redirectUri = `${window.location.origin}/login`;
    return `https://${config.cognitoDomain}/logout?client_id=${config.cognitoClientId}&logout_uri=${encodeURIComponent(redirectUri)}`;
  }

  return '/login';
};

/**
 * Validate that required configuration is present
 * Useful for debugging during hackathon
 */
export const validateConfig = (): { valid: boolean; missing: string[] } => {
  const missing: string[] = [];

  if (!config.apiBaseUrl) {
    missing.push('VITE_API_BASE_URL');
  }

  if (!config.cognitoLoginUrl && !config.cognitoDomain) {
    missing.push('VITE_COGNITO_LOGIN_URL or VITE_COGNITO_DOMAIN');
  }

  return {
    valid: missing.length === 0,
    missing,
  };
};
