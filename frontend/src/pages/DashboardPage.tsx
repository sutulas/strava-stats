import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Stack,
  Link,
} from '@mui/material';
import { apiService, UserStats, DataOverview } from '../services/apiService';

const DashboardPage: React.FC = () => {
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [dataOverview, setDataOverview] = useState<DataOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        const [statsData, overviewData] = await Promise.all([
          apiService.getUserStats(),
          apiService.getDataOverview(),
        ]);
        setUserStats(statsData);
        setDataOverview(overviewData);
      } catch (err) {
        console.error('Error loading dashboard data:', err);
        setError('Failed to load dashboard data. Please try refreshing the page.');
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '50vh',
        }}
      >
        <CircularProgress sx={{ color: '#FC5200' }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 4 }}>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Welcome Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Welcome Back!
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Your running data has been analyzed and is ready for exploration. 
                Use the Analysis page to ask questions about your running performance 
                and get AI-powered insights.
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Link
                  href="https://www.strava.com/dashboard"
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{
                    color: '#FC5200',
                    textDecoration: 'underline',
                    fontWeight: 'bold',
                    fontSize: '0.9rem',
                  }}
                >
                  View on Strava
                </Link>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Stats */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Stats
              </Typography>
              <Stack spacing={2}>
                <Box>
                  <Typography variant="h4" color="primary">
                    {userStats?.summary.total_runs || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Runs
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h4" color="primary">
                    {userStats?.summary.total_miles && userStats.summary.total_miles > 0 
                      ? userStats.summary.total_miles.toFixed(1) 
                      : '0.0'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Miles
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Metrics */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Pace
              </Typography>
              <Typography variant="h3" color="primary">
                {userStats?.averages.avg_pace && userStats.averages.avg_pace > 0 
                  ? userStats.averages.avg_pace.toFixed(1) 
                  : 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                min/mile
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Distance
              </Typography>
              <Typography variant="h3" color="primary">
                {userStats?.averages.avg_distance && userStats.averages.avg_distance > 0 
                  ? userStats.averages.avg_distance.toFixed(1) 
                  : 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                miles
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Heart Rate
              </Typography>
              <Typography variant="h3" color="primary">
                {userStats?.averages.avg_heartrate && userStats.averages.avg_heartrate > 0 
                  ? userStats.averages.avg_heartrate.toFixed(0) 
                  : 'N/A'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                bpm
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Data Overview */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Data Overview
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Activities Analyzed
                  </Typography>
                  <Typography variant="h5">
                    {dataOverview?.total_activities || 0}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Date Range
                  </Typography>
                  <Typography variant="h5">
                    {dataOverview?.date_range.start ? 
                      new Date(dataOverview.date_range.start).getFullYear() : 
                      'N/A'
                    }
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Last Updated
                  </Typography>
                  <Typography variant="h5">
                    {dataOverview?.data_loaded_at ? 
                      new Date(dataOverview.data_loaded_at).toLocaleDateString() : 
                      'N/A'
                    }
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;