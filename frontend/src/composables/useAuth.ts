import { ref, computed } from 'vue';

interface User {
  email: string;
  token: string;
}

// Global auth state
const user = ref<User | null>(null);
const accessToken = ref<string | null>(null);
const isAuthenticated = computed(() => user.value !== null && accessToken.value !== null);

// Check for existing session on load
const initAuth = () => {
  const storedUser = localStorage.getItem('auth_user');
  const storedToken = localStorage.getItem('auth_token');
  
  if (storedUser && storedToken) {
    try {
      user.value = JSON.parse(storedUser);
      accessToken.value = storedToken;
    } catch (error) {
      console.error('Failed to parse stored auth:', error);
      localStorage.removeItem('auth_user');
      localStorage.removeItem('auth_token');
    }
  }
};

// Initialize on module load
initAuth();

export const useAuth = () => {
  const login = async (credentials: { email: string; token: string }) => {
    // TODO: Replace with actual Cognito authentication
    // Example Cognito flow:
    // import { CognitoUserPool, AuthenticationDetails, CognitoUser } from 'amazon-cognito-identity-js';
    // const authenticationData = { Username: email, Password: password };
    // const authenticationDetails = new AuthenticationDetails(authenticationData);
    // const userData = { Username: email, Pool: userPool };
    // const cognitoUser = new CognitoUser(userData);
    // 
    // return new Promise((resolve, reject) => {
    //   cognitoUser.authenticateUser(authenticationDetails, {
    //     onSuccess: (result) => {
    //       const token = result.getIdToken().getJwtToken();
    //       resolve(token);
    //     },
    //     onFailure: (err) => reject(err),
    //   });
    // });
    
    user.value = {
      email: credentials.email,
      token: credentials.token,
    };
    accessToken.value = credentials.token;
    
    localStorage.setItem('auth_user', JSON.stringify(user.value));
    localStorage.setItem('auth_token', credentials.token);
  };

  const logout = () => {
    // TODO: Replace with actual Cognito sign out
    // Example: cognitoUser.signOut();
    
    user.value = null;
    accessToken.value = null;
    localStorage.removeItem('auth_user');
    localStorage.removeItem('auth_token');
  };

<<<<<<< HEAD
  const getAuthToken = (): string | null => {
    return accessToken.value;
=======
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

        const tokens = await response.json();
        storeTokens(tokens.access_token, tokens.id_token);
        return;
      } catch (error) {
        console.error('Token exchange error:', error);
        throw error;
      }
    }

    throw new Error('No authentication code or tokens found');
>>>>>>> f9cd5c7eb3cf119e19d5cdf3765145e9c7274620
  };

  return {
    user: computed(() => user.value),
    accessToken: computed(() => accessToken.value),
    isAuthenticated,
    login,
    logout,
    getAuthToken,
  };
};
