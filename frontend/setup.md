# Strava Authentication Setup Guide

## Step 1: Get Strava API Credentials

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application or use an existing one
3. Note down your **Client ID**
4. Set the **Authorization Callback Domain** to `localhost:4200`

## Step 2: Configure Environment

1. Copy the example environment file:
   ```bash
   cp src/environments/environment.example.ts src/environments/environment.ts
   ```

2. Edit `src/environments/environment.ts` and replace `YOUR_STRAVA_CLIENT_ID` with your actual Client ID

## Step 3: Update Backend Configuration

1. In your backend `.env` file, ensure you have:
   ```
   CLIENT_ID=your_strava_client_id
   CLIENT_SECRET=your_strava_client_secret
   REDIRECT_URI=http://localhost:4200/token
   ```

## Step 4: Test the Setup

1. Start your backend server (should be running on port 8000)
2. Start the frontend: `ng serve`
3. Navigate to `http://localhost:4200`
4. Click "Connect with Strava"
5. Authorize the application on Strava
6. You should be redirected back to the dashboard

## Troubleshooting

- **CORS Errors**: Ensure your backend allows requests from `http://localhost:4200`
- **Redirect URI Mismatch**: Verify the redirect URI in Strava matches exactly
- **Client ID Issues**: Double-check your Client ID in the environment file
- **Backend Connection**: Make sure your backend is running on port 8000

## Security Notes

- Never commit your actual Strava credentials to version control
- Use environment variables for sensitive configuration
- Consider implementing proper session management for production use 