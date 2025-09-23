import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Container,
  Typography,
  Stack,
  CircularProgress,
} from '@mui/material';
import { authService } from '../services/authService';
import { apiService } from '../services/apiService';
import LoadingScreen from '../components/LoadingScreen';

const LoginPage: React.FC = () => {
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [showDataLoading] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      // Wake up the backend service by calling health endpoint
      try {
        await apiService.getHealth();
        console.log('Backend service health check successful');
      } catch (error) {
        console.warn('Backend service health check failed:', error);
        // Continue with auth check even if health check fails
      }

      // Check if user is already authenticated
      if (authService.isAuthenticated()) {
        // If user is already authenticated, go directly to dashboard
        // Data loading will be handled by individual pages as needed
        window.location.href = '/dashboard';
      }
      setIsCheckingAuth(false);
    };

    checkAuth();
  }, []);

  const handleDataLoadingComplete = () => {
    window.location.href = '/dashboard';
  };

  const handleStravaLogin = () => {
    authService.redirectToStravaAuth();
  };

  if (isCheckingAuth) {
    return (
      <Box
        sx={{
          minHeight: '100vh',
          backgroundColor: '#000000',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <CircularProgress sx={{ color: '#FC5200' }} />
      </Box>
    );
  }

  if (showDataLoading) {
    return <LoadingScreen onComplete={handleDataLoadingComplete} />;
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        backgroundColor: '#000000',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 2,
      }}
    >
      <Container maxWidth="sm">
        <Card
          sx={{
            backgroundColor: '#111111',
            border: '1px solid #333333',
            borderRadius: 3,
            padding: 4,
          }}
        >
          <CardContent>
            <Stack spacing={4} alignItems="center">
              {/* Strava Logo
              <Box
                component="img"
                src={stravaLogo}
                alt="Strava Logo"
                sx={{
                  height: 80,
                  width: 'auto',
                }}
              /> */}

              {/* Title */}
              <Typography
                variant="h1"
                component="h1"
                textAlign="center"
                sx={{
                  fontWeight: 800,
                  background: 'linear-gradient(45deg, #FC5200, #ff8a65)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Running Stats
              </Typography>
               {/* Official Powered by Strava Logo
               <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
                <Box
                  component="img"
                  src="/strava-resources/1.2-Strava-API-Logos/Powered by Strava/pwrdBy_strava_white/api_logo_pwrdBy_strava_horiz_white.png"
                  alt="Powered by Strava"
                  sx={{
                    height: 15,
                    width: 'auto',
                    opacity: 0.7,
                  }}
                />
              </Box> */}
              {/* Subtitle */}
              <Typography
                variant="h6"
                textAlign="center"
                color="text.secondary"
                sx={{ maxWidth: 400 }}
              >
                Analyze your running data with AI-powered insights and beautiful visualizations
              </Typography>

              {/* Official Connect with Strava Button */}
              <Box
                component="img"
                src="/strava-resources/1.1 Connect with Strava Buttons/Connect with Strava White/btn_strava_connect_with_white.png"
                alt="Connect with Strava"
                onClick={handleStravaLogin}
                sx={{
                  height: 48,
                  width: 'auto',
                  cursor: 'pointer',
                  transition: 'opacity 0.2s ease',
                  '&:hover': {
                    opacity: 0.8,
                  },
                }}
              />

              {/* Features */}
              <Box sx={{ width: '100%', mt: 4 }}>
                <Typography variant="h6" textAlign="center" mb={2}>
                  Features
                </Typography>
                <Stack spacing={1}>
                  <Typography variant="body2" color="text.secondary" textAlign="center">
                    AI-powered data analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary" textAlign="center">
                    Interactive charts and visualizations
                  </Typography>
                  <Typography variant="body2" color="text.secondary" textAlign="center">
                    Personal running insights
                  </Typography>
                  <Typography variant="body2" color="text.secondary" textAlign="center">
                    Export your data
                  </Typography>
                </Stack>
              </Box>

            </Stack>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
};

export default LoginPage;