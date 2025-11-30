import { ref, computed } from 'vue';
import { config, getCognitoLogoutUrl } from '../config';

interface User {
  email?: string;
  sub?: string;
  [key: string]: any;
}

const accessToken = ref<string | null>(null);
const idToken = ref<string | null>(null);
const user = ref<User | null>(null);

const TOKEN_KEY = 'auth_token';
const ID_TOKEN_KEY = 'id_token';
const USER_KEY = 'auth_user';

export const useAuth = () => {
  const isAuthenticated = computed(() => !!accessToken.value);

  const parseJwt = (token: string): any => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Failed to parse JWT:', error);
      return null;
    }
  };

  const storeTokens = (access: string, id?: string) => {
    accessToken.value = access;
    localStorage.setItem(TOKEN_KEY, access);

    if (id) {
      idToken.value = id;
      localStorage.setItem(ID_TOKEN_KEY, id);

      const userData = parseJwt(id);
      if (userData) {
        user.value = userData;
        localStorage.setItem(USER_KEY, JSON.stringify(userData));
      }
    }
  };

  const clearTokens = () => {
    accessToken.value = null;
    idToken.value = null;
    user.value = null;
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(ID_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  };

  const restoreSession = () => {
    const storedToken = localStorage.getItem(TOKEN_KEY);
    const storedIdToken = localStorage.getItem(ID_TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_KEY);

    if (storedToken) {
      accessToken.value = storedToken;
    }

    if (storedIdToken) {
      idToken.value = storedIdToken;
    }

    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser);
      } catch (error) {
        console.error('Failed to parse stored user:', error);
      }
    }
  };

  const login = () => {
    if (!config.cognitoLoginUrl) {
      console.error('VITE_COGNITO_LOGIN_URL is not configured');
      return;
    }
    window.location.href = config.cognitoLoginUrl;
  };

  const logout = () => {
    clearTokens();
    const logoutUrl = getCognitoLogoutUrl();
    window.location.href = logoutUrl;
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

    if (accessTokenParam) {
      storeTokens(accessTokenParam, idTokenParam || undefined);
      return;
    }

    if (code) {
      if (config.apiBaseUrl) {
        try {
          const response = await fetch(`${config.apiBaseUrl}/auth/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code }),
          });

          if (!response.ok) {
            throw new Error('Token exchange failed');
          }

          const data = await response.json();
          storeTokens(data.access_token, data.id_token);
          return;
        } catch (error) {
          console.error('Token exchange error:', error);
          throw error;
        }
      }

      throw new Error('API URL not configured for token exchange');
    }

    throw new Error('No authentication code or tokens found');
  };

  restoreSession();

  return {
    isAuthenticated,
    user,
    accessToken,
    login,
    logout,
    handleCallback,
  };
};
