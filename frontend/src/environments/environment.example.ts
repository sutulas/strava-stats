// Copy this file to environment.ts and update with your actual Strava API credentials
export const environment = {
  production: false,
  strava: {
    clientId: 'YOUR_STRAVA_CLIENT_ID', // Get this from https://www.strava.com/settings/api
    redirectUri: 'http://localhost:4200/token'
  }
}; 