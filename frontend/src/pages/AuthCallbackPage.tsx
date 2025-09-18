import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Stack,
  Button,
} from '@mui/material';
import { authService } from '../services/authService';
import LoadingScreen from '../components/LoadingScreen';

const AuthCallbackPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDataLoading, setShowDataLoading] = useState(false);

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        const code = searchParams.get('code');
        const error = searchParams.get('error');

        if (error) {
          setError('Authentication failed. Please try again.');
          setLoading(false);
          return;
        }

        if (!code) {
          setError('No authorization code received.');
          setLoading(false);
          return;
        }

        // Exchange code for token
        await authService.handleAuthCallback(code);

        // Show data loading screen
        setShowDataLoading(true);
        setLoading(false);
      } catch (err) {
        console.error('Auth callback error:', err);
        setError('Failed to authenticate with Strava. Please try again.');
        setLoading(false);
      }
    };

    handleAuthCallback();
  }, [searchParams, navigate]);

  const handleDataLoadingComplete = () => {
    navigate('/dashboard');
  };

  if (showDataLoading) {
    return <LoadingScreen onComplete={handleDataLoadingComplete} />;
  }

  if (loading) {
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
        <Card
          sx={{
            backgroundColor: '#111111',
            border: '1px solid #333333',
            borderRadius: 3,
            padding: 4,
          }}
        >
          <CardContent>
            <Stack spacing={3} alignItems="center">
              <CircularProgress sx={{ color: '#ff6b35' }} />
              <Typography variant="h6" textAlign="center">
                Connecting to Strava...
              </Typography>
              <Typography variant="body2" color="text.secondary" textAlign="center">
                Please wait while we authenticate your account and load your data.
              </Typography>
            </Stack>
          </CardContent>
        </Card>
      </Box>
    );
  }

  if (error) {
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
        <Card
          sx={{
            backgroundColor: '#111111',
            border: '1px solid #333333',
            borderRadius: 3,
            padding: 4,
          }}
        >
          <CardContent>
            <Stack spacing={3} alignItems="center">
              <Alert severity="error" sx={{ width: '100%' }}>
                {error}
              </Alert>
              <Button
                variant="contained"
                onClick={() => navigate('/login')}
                sx={{
                  backgroundColor: '#ff6b35',
                  '&:hover': {
                    backgroundColor: '#e64a19',
                  },
                }}
              >
                Try Again
              </Button>
            </Stack>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return null;
};

export default AuthCallbackPage;