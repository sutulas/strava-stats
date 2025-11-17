import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Avatar,
  CircularProgress,
  Alert,
  Stack,
  Chip,
  Link,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { apiService, UserProfile, UserStats } from '../services/apiService';
import { authService } from '../services/authService';
import { useNavigate } from 'react-router-dom';

const ProfilePage: React.FC = () => {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const loadProfileData = async () => {
      try {
        setLoading(true);
        const [profileData, statsData] = await Promise.all([
          apiService.getUserProfile(),
          apiService.getUserStats(),
        ]);
        setUserProfile(profileData);
        setUserStats(statsData);
      } catch (err) {
        console.error('Error loading profile data:', err);
        setError('Failed to load profile data. Please try refreshing the page.');
      } finally {
        setLoading(false);
      }
    };

    loadProfileData();
  }, []);

  const handleDeleteData = async () => {
    try {
      setDeleting(true);
      const result = await apiService.deleteUserData();
      console.log('Data deletion result:', result);
      
      // Clear local storage and redirect to login
      authService.logout();
      navigate('/login');
    } catch (err) {
      console.error('Error deleting data:', err);
      setError('Failed to delete data. Please try again.');
    } finally {
      setDeleting(false);
      setDeleteDialogOpen(false);
    }
  };

  const handleDeleteDialogOpen = () => {
    setDeleteDialogOpen(true);
  };

  const handleDeleteDialogClose = () => {
    setDeleteDialogOpen(false);
  };

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

  // Prepare chart data
  const weeklyData = userStats?.weekly_stats?.map((week, index) => ({
    week: `Week ${index + 1}`,
    miles: week.miles ? parseFloat(week.miles.toFixed(2)) : 0,
  })) || [];

  const monthlyData = userStats?.monthly_stats?.map(month => ({
    month: month.month,
    runs: month.runs || 0,
  })) || [];

  const dayOfWeekData = userStats?.day_of_week_stats?.map(day => ({
    day: day.day,
    runs: day.runs || 0,
    miles: day.miles || 0,
    avg_distance: day.avg_distance || 0,
    avg_pace: day.avg_pace || 0,
    total_time: day.total_time || 0,
  })) || [];

  const COLORS = ['#FC5200', '#ff8a65', '#ffab91', '#ffccbc', '#ffe0b2'];

  // Debug logging
  console.log('Profile data:', { userStats, weeklyData, monthlyData, dayOfWeekData });

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 2 }}>
        Profile
      </Typography>

      <Grid container spacing={2}>
        {/* User Info Card */}
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Stack spacing={2} alignItems="center">
                <Avatar
                  src={userProfile?.profile}
                  sx={{ width: 80, height: 80 }}
                />
                <Box textAlign="center">
                  <Typography variant="h6" gutterBottom>
                    {userProfile?.firstname} {userProfile?.lastname}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    @{userProfile?.username}
                  </Typography>
                  <Chip
                    label={`${userProfile?.city}, ${userProfile?.state}`}
                    variant="outlined"
                    size="small"
                    sx={{ mt: 0.5 }}
                  />
                  <Box sx={{ mt: 1.5 }}>
                    <Link
                      href={`https://www.strava.com/athletes/${userProfile?.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      sx={{
                        color: '#FC5200',
                        textDecoration: 'underline',
                        fontWeight: 'bold',
                        fontSize: '0.8rem',
                      }}
                    >
                      View on Strava
                    </Link>
                  </Box>
                  <Box sx={{ mt: 1.5 }}>
                    <Button
                      variant="outlined"
                      color="error"
                      size="small"
                      onClick={handleDeleteDialogOpen}
                      sx={{
                        borderColor: '#f44336',
                        color: '#f44336',
                        fontSize: '0.75rem',
                        '&:hover': {
                          borderColor: '#d32f2f',
                          backgroundColor: 'rgba(244, 67, 54, 0.1)',
                        },
                      }}
                    >
                      Delete My Data
                    </Button>
                  </Box>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Stats */}
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1.5 }}>
                Quick Stats
              </Typography>
              <Stack spacing={1.5}>
                <Box>
                  <Typography variant="h5" color="primary" sx={{ fontSize: '1.75rem' }}>
                    {userStats?.summary.total_runs || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                    Total Runs
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h5" color="primary" sx={{ fontSize: '1.75rem' }}>
                    {userStats?.summary.total_miles && userStats.summary.total_miles > 0 
                      ? userStats.summary.total_miles.toFixed(1) 
                      : '0.0'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                    Total Miles
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Average Stats */}
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1.5 }}>
                Average Stats
              </Typography>
              <Stack spacing={1.5}>
                <Box>
                  <Typography variant="h6" color="primary" sx={{ fontSize: '1.5rem' }}>
                    {userStats?.averages.avg_pace && userStats.averages.avg_pace > 0 
                      ? userStats.averages.avg_pace.toFixed(1) 
                      : 'N/A'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                    Avg Pace (min/mi)
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h6" color="primary" sx={{ fontSize: '1.5rem' }}>
                    {userStats?.averages.avg_distance && userStats.averages.avg_distance > 0 
                      ? userStats.averages.avg_distance.toFixed(1) 
                      : 'N/A'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                    Avg Distance (mi)
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h6" color="primary" sx={{ fontSize: '1.5rem' }}>
                    {userStats?.averages.avg_heartrate && userStats.averages.avg_heartrate > 0 
                      ? userStats.averages.avg_heartrate.toFixed(0) 
                      : 'N/A'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                    Avg Heart Rate (bpm)
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Running Statistics */}
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1.5 }}>
                Running Statistics
              </Typography>
              <Stack spacing={1.5}>
                <Box>
                  <Typography variant="h6" color="primary" sx={{ fontSize: '1.5rem' }}>
                    {userStats?.summary.total_time_minutes?.toFixed(0) || '0'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                    Total Minutes
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h6" color="primary" sx={{ fontSize: '1.5rem' }}>
                    {userStats?.summary.total_elevation?.toFixed(0) || '0'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                    Total Elevation (ft)
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Weekly Mileage Chart */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1 }}>
                Weekly Mileage Trend
              </Typography>
              {weeklyData.length > 0 ? (
                <Box height={250}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={weeklyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333333" />
                      <XAxis dataKey="week" stroke="#aaaaaa" />
                      <YAxis stroke="#aaaaaa" />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#111111',
                          border: '1px solid #333333',
                          color: '#ffffff',
                        }}
                      />
                      <Line
                        type="monotone"
                        dataKey="miles"
                        stroke="#FC5200"
                        strokeWidth={3}
                        dot={{ fill: '#FC5200', strokeWidth: 2, r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Box>
              ) : (
                <Box height={250} display="flex" alignItems="center" justifyContent="center">
                  <Typography color="text.secondary" sx={{ fontSize: '0.875rem' }}>No weekly data available</Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Monthly Runs Chart */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1 }}>
                Monthly Runs
              </Typography>
              {monthlyData.length > 0 ? (
                <Box height={250}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={monthlyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333333" />
                      <XAxis dataKey="month" stroke="#aaaaaa" />
                      <YAxis stroke="#aaaaaa" />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#111111',
                          border: '1px solid #333333',
                          color: '#ffffff',
                        }}
                      />
                      <Bar dataKey="runs" fill="#FC5200" />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
              ) : (
                <Box height={250} display="flex" alignItems="center" justifyContent="center">
                  <Typography color="text.secondary" sx={{ fontSize: '0.875rem' }}>No monthly data available</Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Day of Week Distribution */}
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1 }}>
                Running by Day of Week
              </Typography>
              {dayOfWeekData.length > 0 ? (
                <Box height={250}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={dayOfWeekData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ day, percent }: any) => `${day} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="runs"
                      >
                        {dayOfWeekData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip
                        content={({ active, payload }) => {
                          if (active && payload && payload.length) {
                            const data = payload[0].payload;
                            return (
                              <div style={{
                                backgroundColor: '#111111',
                                border: '1px solid #333333',
                                borderRadius: '4px',
                                padding: '8px 12px',
                                color: '#ffffff',
                                fontSize: '14px',
                              }}>
                                <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                                  {data.day}
                                </div>
                                <div>Runs: {data.runs}</div>
                                <div>Total Miles: {data.miles?.toFixed(2) || '0.00'}</div>
                                <div>Avg Distance: {data.avg_distance?.toFixed(2) || '0.00'} mi</div>
                              </div>
                            );
                          }
                          return null;
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
              ) : (
                <Box height={250} display="flex" alignItems="center" justifyContent="center">
                  <Typography color="text.secondary" sx={{ fontSize: '0.875rem' }}>No day-of-week data available</Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Delete Data Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteDialogClose}
        PaperProps={{
          sx: {
            backgroundColor: '#111111',
            border: '1px solid #333333',
          },
        }}
      >
        <DialogTitle sx={{ color: '#ffffff' }}>
          Delete All My Data
        </DialogTitle>
        <DialogContent>
          <DialogContentText sx={{ color: '#cccccc' }}>
            This action will permanently delete all your data from our servers, including:
            <br />
            • Your running activity data
            <br />
            • Generated charts and analysis
            <br />
            • All cached information
            <br />
            <br />
            <strong>This action cannot be undone.</strong> You will be logged out and redirected to the login page.
            <br />
            <br />
            If you want to continue using the service, you can simply log out without deleting your data.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={handleDeleteDialogClose}
            disabled={deleting}
            sx={{ color: '#FC5200' }}
          >
            Cancel
          </Button>
          <Button
            onClick={handleDeleteData}
            disabled={deleting}
            variant="contained"
            color="error"
            sx={{
              backgroundColor: '#f44336',
              '&:hover': {
                backgroundColor: '#d32f2f',
              },
            }}
          >
            {deleting ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1 }} />
                Deleting...
              </>
            ) : (
              'Delete All Data'
            )}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProfilePage;