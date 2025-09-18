# Running Stats Frontend

A modern React frontend for analyzing Strava running data with AI-powered insights.

## Features

- **Dark Theme Design**: Clean, modern interface with dark theme and orange accents
- **Strava Authentication**: Secure OAuth integration with Strava
- **AI-Powered Analysis**: Natural language queries about your running data
- **Interactive Charts**: Beautiful visualizations using Recharts
- **Data Management**: View, refresh, and download your running data
- **Responsive Design**: Works on desktop and mobile devices

## Pages

1. **Login Page**: Strava OAuth authentication with proper branding
2. **Dashboard**: Overview of your running statistics and quick metrics
3. **Profile**: Personal information and running charts
4. **Analysis**: AI-powered query interface for data insights
5. **Data**: Data management and download functionality

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file with your Strava API credentials:
   ```bash
   cp .env.example .env
   ```
   
   Then edit the `.env` file with your actual values:
   ```
   # Get these from https://www.strava.com/settings/api
   REACT_APP_STRAVA_CLIENT_ID=your_strava_client_id
   REACT_APP_REDIRECT_URI=http://localhost:3000/auth/callback
   REACT_APP_API_BASE_URL=http://localhost:8000
   REACT_APP_ENVIRONMENT=development
   ```
   
   **Note**: You need to create a Strava API application at https://www.strava.com/settings/api to get your client ID and set up the redirect URI.

3. Start the development server:
   ```bash
   npm start
   ```

## Tech Stack

- **React 18** with TypeScript
- **Material-UI** for components and theming
- **React Router** for navigation
- **Recharts** for data visualization
- **Axios** for API communication

## Design System

- **Colors**: Black background (#000000), white text (#ffffff), orange accents (#ff6b35)
- **Typography**: Inter/Roboto/Poppins font family
- **Layout**: Sidebar navigation with main content area
- **Components**: Cards, buttons, and forms with consistent styling

## API Integration

The frontend integrates with the Strava Stats backend API:
- Authentication endpoints
- User profile and statistics
- AI-powered query processing
- Chart generation
- Data management

## Strava Compliance

- Uses official Strava logo and branding
- Includes "Built with Strava" attribution
- Follows Strava API guidelines
- Proper OAuth 2.0 implementation