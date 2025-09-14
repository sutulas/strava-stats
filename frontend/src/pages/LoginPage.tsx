import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
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
import stravaLogo from '../assets/strava-2.svg';

const LoginPage: React.FC = () => {
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [showDataLoading, setShowDataLoading] = useState(false);

  useEffect(() => {
    const checkAuthAndData = async () => {
      // Check if user is already authenticated
      if (authService.isAuthenticated()) {
        try {
          // Check if data needs to be loaded
          const dataStatus = await apiService.getDataStatus();
          if (!dataStatus.data_processed || !dataStatus.workflow_ready) {
            setShowDataLoading(true);
          } else {
            window.location.href = '/dashboard';
          }
        } catch (error) {
          console.error('Error checking data status:', error);
          // If there's an error, proceed to dashboard anyway
          window.location.href = '/dashboard';
        }
      }
      setIsCheckingAuth(false);
    };

    checkAuthAndData();
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
        <CircularProgress sx={{ color: '#ff6b35' }} />
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
              {/* Strava Logo */}
              <Box
                component="img"
                src={stravaLogo}
                alt="Strava Logo"
                sx={{
                  height: 80,
                  width: 'auto',
                }}
              />

              {/* Title */}
              <Typography
                variant="h3"
                component="h1"
                textAlign="center"
                sx={{
                  fontWeight: 700,
                  background: 'linear-gradient(45deg, #ff6b35, #ff8a65)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                Strava Stats
              </Typography>

              {/* Subtitle */}
              <Typography
                variant="h6"
                textAlign="center"
                color="text.secondary"
                sx={{ maxWidth: 400 }}
              >
                Analyze your running data with AI-powered insights and beautiful visualizations
              </Typography>

              {/* Built with Strava */}
              <Typography
                variant="body2"
                color="text.secondary"
                textAlign="center"
                sx={{ fontStyle: 'italic' }}
              >
                Built with Strava
              </Typography>

              {/* Login Button */}
              <Button
                variant="contained"
                size="large"
                onClick={handleStravaLogin}
                sx={{
                  backgroundColor: '#fc4c02',
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '1.1rem',
                  padding: '12px 32px',
                  borderRadius: 2,
                  textTransform: 'none',
                  '&:hover': {
                    backgroundColor: '#e03e00',
                  },
                }}
              >
                Connect with Strava
              </Button>

              {/* Features */}
              <Box sx={{ width: '100%', mt: 4 }}>
                <Typography variant="h6" textAlign="center" mb={2}>
                  Features
                </Typography>
                <Stack spacing={1}>
                  <Typography variant="body2" color="text.secondary">
                    • AI-powered data analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Interactive charts and visualizations
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Personal running insights
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Export your data
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