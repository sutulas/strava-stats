# Strava Stats Frontend

This is the frontend application for Strava Stats, built with Angular and Tailwind CSS.

## Features

- **Strava Authentication**: Secure OAuth2 login with Strava
- **Dashboard**: View your Strava activity statistics
- **Data Analysis**: Query and analyze your fitness data
- **Data Overview**: Comprehensive view of your activities
- **Responsive Design**: Modern, mobile-friendly interface

## Setup

### Prerequisites

- Node.js (v16 or higher)
- Angular CLI (`npm install -g @angular/cli`)
- Strava API credentials

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure Strava API credentials:
   - Create a Strava API application at [Strava API Settings](https://www.strava.com/settings/api)
   - Copy your Client ID
   - Update `src/environments/environment.ts` with your Client ID:
     ```typescript
     export const environment = {
       production: false,
       strava: {
         clientId: 'YOUR_ACTUAL_CLIENT_ID',
         redirectUri: 'http://localhost:4200/token'
       }
     };
     ```

3. Start the development server:
   ```bash
   ng serve
   ```

4. Open your browser and navigate to `http://localhost:4200`

## Authentication Flow

1. **Login Page**: Users click "Connect with Strava" button
2. **Strava OAuth**: User is redirected to Strava to authorize the application
3. **Callback**: Strava redirects back to `/token` with an authorization code
4. **Token Exchange**: The backend exchanges the code for access tokens
5. **Dashboard**: User is redirected to the dashboard with full access

## Backend Integration

The frontend expects a backend service running on `http://localhost:8000` with the following endpoints:

- `POST /auth/token` - Exchange authorization code for tokens
- `GET /activities` - Retrieve user activities
- `GET /profile` - Get user profile information

## Development

### Project Structure

```
src/
├── app/
│   ├── login/              # Login component
│   ├── token-callback/     # OAuth callback handler
│   ├── dashboard/          # Main dashboard
│   ├── services/           # API services
│   └── shared/             # Shared components
├── environments/            # Environment configuration
└── assets/                 # Static assets
```

### Key Components

- **LoginComponent**: Handles initial Strava authentication
- **TokenCallbackComponent**: Processes OAuth callback and token exchange
- **StravaAuthService**: Manages authentication state and tokens
- **StravaDataService**: Handles API communication with backend

### Environment Configuration

- `environment.ts` - Development configuration
- `environment.prod.ts` - Production configuration

## Building for Production

```bash
ng build --configuration production
```

## Troubleshooting

- **CORS Issues**: Ensure your backend allows requests from `http://localhost:4200`
- **Authentication Errors**: Check that your Strava Client ID is correct
- **Redirect Issues**: Verify the redirect URI matches your Strava API settings

## Security Notes

- Never commit API keys or secrets to version control
- Use environment variables for sensitive configuration
- Implement proper token storage and refresh mechanisms
- Consider implementing route guards for protected routes 