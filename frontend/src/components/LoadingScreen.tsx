import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Stack,
  LinearProgress,
} from '@mui/material';
import { apiService } from '../services/apiService';

interface LoadingScreenProps {
  onComplete: () => void;
}

interface LoadingStep {
  id: string;
  label: string;
  completed: boolean;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [steps, setSteps] = useState<LoadingStep[]>([
    { id: 'profile', label: 'Loading user profile...', completed: false },
    { id: 'data', label: 'Refreshing activity data...', completed: false },
    { id: 'stats', label: 'Calculating statistics...', completed: false },
    { id: 'overview', label: 'Preparing data overview...', completed: false },
  ]);

  useEffect(() => {
    const loadAllData = async () => {
      try {
        // Step 1: Load user profile
        setCurrentStep(0);
        await apiService.getUserProfile();
        setSteps(prev => prev.map((step, index) => 
          index === 0 ? { ...step, completed: true } : step
        ));

        // Step 2: Refresh data
        setCurrentStep(1);
        await apiService.refreshData();
        setSteps(prev => prev.map((step, index) => 
          index === 1 ? { ...step, completed: true } : step
        ));

        // Step 3: Load user stats
        setCurrentStep(2);
        await apiService.getUserStats();
        setSteps(prev => prev.map((step, index) => 
          index === 2 ? { ...step, completed: true } : step
        ));

        // Step 4: Load data overview
        setCurrentStep(3);
        await apiService.getDataOverview();
        setSteps(prev => prev.map((step, index) => 
          index === 3 ? { ...step, completed: true } : step
        ));

        // All data loaded
        setTimeout(() => {
          onComplete();
        }, 500); // Small delay to show completion

      } catch (error) {
        console.error('Error loading data:', error);
        // Even if there's an error, proceed to the app
        // Individual pages will handle their own error states
        setTimeout(() => {
          onComplete();
        }, 1000);
      }
    };

    loadAllData();
  }, [onComplete]);

  const completedSteps = steps.filter(step => step.completed).length;
  const progress = (completedSteps / steps.length) * 100;

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
      <Card
        sx={{
          backgroundColor: '#111111',
          border: '1px solid #333333',
          borderRadius: 3,
          padding: 4,
          maxWidth: 500,
          width: '100%',
        }}
      >
        <CardContent>
          <Stack spacing={4} alignItems="center">
            {/* Title */}
            <Typography
              variant="h4"
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

            {/* Main loading indicator */}
            <Box sx={{ position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CircularProgress 
                size={80} 
                thickness={4}
                sx={{ 
                  color: '#ff6b35',
                  position: 'absolute',
                }} 
              />
              <Typography
                variant="h6"
                sx={{
                  fontWeight: 600,
                  color: '#ff6b35',
                }}
              >
                {Math.round(progress)}%
              </Typography>
            </Box>

            {/* Progress bar */}
            <Box sx={{ width: '100%' }}>
              <LinearProgress
                variant="determinate"
                value={progress}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: '#333333',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#ff6b35',
                    borderRadius: 4,
                  },
                }}
              />
            </Box>

            {/* Current step */}
            <Typography variant="h6" textAlign="center" color="primary">
              {steps[currentStep]?.label || 'Preparing your dashboard...'}
            </Typography>

            {/* Step indicators */}
            <Stack spacing={1} sx={{ width: '100%' }}>
              {steps.map((step, index) => (
                <Box
                  key={step.id}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 2,
                    padding: 1,
                    borderRadius: 1,
                    backgroundColor: step.completed ? '#1a4d1a' : '#333333',
                    transition: 'all 0.3s ease',
                  }}
                >
                  <CircularProgress
                    size={20}
                    variant={step.completed ? 'determinate' : 'indeterminate'}
                    value={100}
                    sx={{
                      color: step.completed ? '#4caf50' : '#ff6b35',
                    }}
                  />
                  <Typography
                    variant="body2"
                    color={step.completed ? 'success.main' : 'text.secondary'}
                    sx={{
                      textDecoration: step.completed ? 'line-through' : 'none',
                      opacity: step.completed ? 0.7 : 1,
                    }}
                  >
                    {step.label}
                  </Typography>
                </Box>
              ))}
            </Stack>

            {/* Subtitle */}
            <Typography
              variant="body2"
              color="text.secondary"
              textAlign="center"
              sx={{ fontStyle: 'italic' }}
            >
              Setting up your personalized running analytics...
            </Typography>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  );
};

export default LoadingScreen;