import { ref, computed } from 'vue';
import { config } from '../config';

interface User {
  email: string;
  token: string;
}

interface TokenResponse {
  access_token: string;
  id_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in: number;
}

// Global auth state
const user = ref<User | null>(null);
const accessToken = ref<string | null>(null);
const idToken = ref<string | null>(null);
const isAuthenticated = computed(() => user.value !== null && accessToken.value !== null);

// Check for existing session on load
const initAuth = () => {
  const storedUser = localStorage.getItem('auth_user');
  const storedAccessToken = localStorage.getItem('auth_access_token');
  const storedIdToken = localStorage.getItem('auth_id_token');
  
  if (storedUser && storedAccessToken) {
    try {
      user.value = JSON.parse(storedUser);
      accessToken.value = storedAccessToken;
      idToken.value = storedIdToken;
    } catch (error) {
      console.error('Failed to parse stored auth:', error);
      clearAuthStorage();
    }
  }
};

const clearAuthStorage = () => {
  localStorage.removeItem('auth_user');
  localStorage.removeItem('auth_access_token');
  localStorage.removeItem('auth_id_token');
};

const storeTokens = (access: string, id?: string) => {
  accessToken.value = access;
  idToken.value = id || null;
  
  localStorage.setItem('auth_access_token', access);
  if (id) {
    localStorage.setItem('auth_id_token', id);
  }
  
  // Decode ID token to get user info
  if (id) {
    try {
      const payload = JSON.parse(atob(id.split('.')[1]));
      user.value = {
        email: payload.email || payload.sub,
        token: access,
      };
      localStorage.setItem('auth_user', JSON.stringify(user.value));
    } catch (error) {
      console.error('Failed to decode ID token:', error);
    }
  }
};

// Initialize on module load
initAuth();

export const useAuth = () => {
  const login = async (credentials: { email: string; token: string }) => {
    // For demo/testing purposes - direct token storage
    user.value = {
      email: credentials.email,
      token: credentials.token,
    };
    accessToken.value = credentials.token;
    
    localStorage.setItem('auth_user', JSON.stringify(user.value));
    localStorage.setItem('auth_access_token', credentials.token);
  };

  const logout = () => {
    user.value = null;
    accessToken.value = null;
    idToken.value = null;
    clearAuthStorage();
  };

  const getAuthToken = (): string | null => {
    return accessToken.value;
  };

  const handleCallback = async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const hashParams = new URLSearchParams(window.location.hash.substring(1));

    const code = urlParams.get('code');
    const accessTokenParam = hashParams.get('access_token') || urlParams.get('access_token');
    const idTokenParam = hashParams.get('id_token') || urlParams.get('id_token');
    const error = urlParams.get('error');

    if (error) {
      throw new Error(urlParams.get('error_description') || 'Authentication failed');
    }

    // If tokens are in URL (implicit flow), store them directly
    if (accessTokenParam) {
      storeTokens(accessTokenParam, idTokenParam || undefined);
      return;
    }

    // If we have an authorization code, exchange it for tokens
    if (code) {
      const cognitoDomain = config.cognitoDomain;
      const clientId = config.cognitoClientId;
      const redirectUri = `${window.location.origin}/login-callback`;

      if (!cognitoDomain || !clientId) {
        throw new Error('Cognito configuration missing');
      }

      try {
        const response = await fetch(`https://${cognitoDomain}/oauth2/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            grant_type: 'authorization_code',
            client_id: clientId,
            code: code,
            redirect_uri: redirectUri,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.error_description || 'Token exchange failed');
        }

        const tokens: TokenResponse = await response.json();
        storeTokens(tokens.access_token, tokens.id_token);
        return;
      } catch (error) {
        console.error('Token exchange error:', error);
        throw error;
      }
    }

    throw new Error('No authentication code or tokens found');
  };

  return {
    user: computed(() => user.value),
    accessToken: computed(() => accessToken.value),
    isAuthenticated,
    login,
    logout,
    getAuthToken,
    handleCallback,
  };
};
