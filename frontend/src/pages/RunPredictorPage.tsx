import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  TextField,
  Button,
  CircularProgress,
  Alert,
  Stack,
} from '@mui/material';
import { apiService, PacePredictionResponse, UserStats } from '../services/apiService';

const RunPredictorPage: React.FC = () => {
  const [distance, setDistance] = useState<string>('5.0');
  const [heartRate, setHeartRate] = useState<string>('150');
  const [prediction, setPrediction] = useState<PacePredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userStats, setUserStats] = useState<UserStats | null>(null);

  useEffect(() => {
    const loadUserStats = async () => {
      try {
        const stats = await apiService.getUserStats();
        setUserStats(stats);
        // Set default heart rate to user's average if available
        if (stats?.averages?.avg_heartrate && stats.averages.avg_heartrate > 0) {
          setHeartRate(stats.averages.avg_heartrate.toFixed(0));
        }
      } catch (err) {
        console.error('Error loading user stats:', err);
      }
    };
    loadUserStats();
  }, []);

  const handlePredict = async () => {
    const distanceNum = parseFloat(distance);
    const heartRateNum = parseFloat(heartRate);

    // Validation
    if (isNaN(distanceNum) || distanceNum <= 0) {
      setError('Please enter a valid distance greater than 0');
      return;
    }

    if (isNaN(heartRateNum) || heartRateNum <= 0 || heartRateNum > 220) {
      setError('Please enter a valid heart rate between 1 and 220 bpm');
      return;
    }

    setError(null);
    setLoading(true);
    setPrediction(null);

    try {
      const result = await apiService.predictPace({
        distance: distanceNum,
        heart_rate: heartRateNum,
      });
      setPrediction(result);
    } catch (err: any) {
      console.error('Error predicting pace:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to predict pace. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (minutes: number): string => {
    const hours = Math.floor(minutes / 60);
    const mins = Math.floor(minutes % 60);
    const secs = Math.floor((minutes % 1) * 60);
    
    if (hours > 0) {
      return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatPace = (paceMinutes: number): string => {
    const minutes = Math.floor(paceMinutes);
    const seconds = Math.floor((paceMinutes % 1) * 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 2 }}>
        Run Predictor
      </Typography>

      <Grid container spacing={2}>
        {/* Input Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 2 }}>
                Run Parameters
              </Typography>
              <Stack spacing={2}>
                <TextField
                  label="Distance (miles)"
                  type="number"
                  value={distance}
                  onChange={(e) => setDistance(e.target.value)}
                  fullWidth
                  inputProps={{ min: 0.1, step: 0.1 }}
                  helperText="Enter the distance you plan to run"
                />
                <TextField
                  label="Target Heart Rate (bpm)"
                  type="number"
                  value={heartRate}
                  onChange={(e) => setHeartRate(e.target.value)}
                  fullWidth
                  inputProps={{ min: 1, max: 220, step: 1 }}
                  helperText={
                    userStats?.averages?.avg_heartrate
                      ? `Your average heart rate: ${userStats.averages.avg_heartrate.toFixed(0)} bpm`
                      : 'Enter your target heart rate'
                  }
                />
                <Button
                  variant="contained"
                  onClick={handlePredict}
                  disabled={loading}
                  fullWidth
                  sx={{
                    backgroundColor: '#FC5200',
                    '&:hover': {
                      backgroundColor: '#e64a19',
                    },
                    mt: 1,
                  }}
                >
                  {loading ? (
                    <>
                      <CircularProgress size={20} sx={{ mr: 1, color: '#ffffff' }} />
                      Predicting...
                    </>
                  ) : (
                    'Predict Pace'
                  )}
                </Button>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Prediction Results Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 2 }}>
                Prediction Results
              </Typography>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              {prediction?.error && (
                <Alert severity="warning" sx={{ mb: 2 }}>
                  {prediction.error}
                </Alert>
              )}
              {prediction && !prediction.error && (
                <Stack spacing={2}>
                  <Box>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                      Predicted Pace
                    </Typography>
                    <Typography variant="h4" color="primary" sx={{ fontSize: '2rem', fontWeight: 'bold' }}>
                      {prediction.predicted_pace ? formatPace(prediction.predicted_pace) : 'N/A'} min/mile
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                      Predicted Time
                    </Typography>
                    <Typography variant="h5" color="primary" sx={{ fontSize: '1.5rem' }}>
                      {prediction.predicted_time_minutes && formatTime(prediction.predicted_time_minutes)}
                    </Typography>
                    {prediction.predicted_time_hours && prediction.predicted_time_hours >= 1 && (
                      <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem', mt: 0.5 }}>
                        ({prediction.predicted_time_hours.toFixed(2)} hours)
                      </Typography>
                    )}
                  </Box>
                  <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid #333333' }}>
                    <Grid container spacing={1}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                          Distance
                        </Typography>
                        <Typography variant="body1" sx={{ fontSize: '0.875rem' }}>
                          {prediction.desired_distance} miles
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                          Heart Rate
                        </Typography>
                        <Typography variant="body1" sx={{ fontSize: '0.875rem' }}>
                          {prediction.desired_heart_rate} bpm
                        </Typography>
                      </Grid>
                      {prediction.runs_used && (
                        <Grid item xs={12}>
                          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                            Based on last {prediction.runs_used} runs
                          </Typography>
                        </Grid>
                      )}
                    </Grid>
                  </Box>
                </Stack>
              )}
              {!prediction && !loading && !error && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body2" color="text.secondary">
                    Enter your run parameters and click "Predict Pace" to get started
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Info Card */}
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1.5 }}>
                How It Works
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem', mb: 1 }}>
                The Run Predictor uses machine learning to predict your running pace based on:
              </Typography>
              <Stack spacing={0.5} sx={{ pl: 2 }}>
                <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem' }}>
                  • Your last 7 runs (distance, pace, elevation, heart rate)
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem' }}>
                  • Your planned run distance
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem' }}>
                  • Your target heart rate
                </Typography>
              </Stack>
              <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem', mt: 1.5 }}>
                <strong>Note:</strong> You need at least 7 previous runs in your data for predictions to work.
                Make sure your data is up to date by refreshing it on the Data page.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RunPredictorPage;

