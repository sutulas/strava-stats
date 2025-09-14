import { apiService } from './apiService';

// export const environment = {
//   production: false,
//   strava: {
//     clientId: '169809',
//     redirectUri: 'http://localhost:4200/token'
//   }
// }; 

const STRAVA_CLIENT_ID = process.env.REACT_APP_STRAVA_CLIENT_ID || '169809';
const REDIRECT_URI = process.env.REACT_APP_REDIRECT_URI || 'http://localhost:3000/auth/callback';
const STRAVA_AUTH_URL = 'https://www.strava.com/oauth/authorize';

class AuthService {
  redirectToStravaAuth(): void {
    const authUrl = `${STRAVA_AUTH_URL}?client_id=${STRAVA_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&approval_prompt=force&scope=activity:read_all`;
    window.location.href = authUrl;
  }

  async handleAuthCallback(code: string) {
    try {
      const response = await apiService.exchangeCodeForToken(code);
      localStorage.setItem('strava_access_token', response.access_token);
      return response;
    } catch (error) {
      console.error('Auth callback error:', error);
      throw error;
    }
  }

  getAccessToken(): string | null {
    return localStorage.getItem('strava_access_token');
  }

  clearTokens(): void {
    localStorage.removeItem('strava_access_token');
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  logout(): void {
    this.clearTokens();
    window.location.href = '/login';
  }
}

export const authService = new AuthService();