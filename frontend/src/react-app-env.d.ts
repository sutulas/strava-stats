/// <reference types="react-scripts" />

declare namespace NodeJS {
  interface ProcessEnv {
    REACT_APP_STRAVA_CLIENT_ID: string;
    REACT_APP_REDIRECT_URI: string;
    REACT_APP_API_BASE_URL: string;
    REACT_APP_ENVIRONMENT: 'development' | 'production' | 'test';
  }
}