import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  CircularProgress,
  Alert,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Link,
} from '@mui/material';
import { Download, Refresh } from '@mui/icons-material';
import { apiService, DataOverview } from '../services/apiService';

const DataPage: React.FC = () => {
  const [dataOverview, setDataOverview] = useState<DataOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const overviewData = await apiService.getDataOverview();
      setDataOverview(overviewData);
    } catch (err) {
      console.error('Error loading data overview:', err);
      setError('Failed to load data overview. Please try refreshing the page.');
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshData = async () => {
    try {
      setRefreshing(true);
      await apiService.refreshData();
      await loadData();
    } catch (err) {
      console.error('Error refreshing data:', err);
      setError('Failed to refresh data. Please try again.');
    } finally {
      setRefreshing(false);
    }
  };

  const handleDownloadData = async () => {
    try {
      // Create a CSV download link
      const csvContent = generateCSVContent();
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `strava-data-${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading data:', err);
      setError('Failed to download data. Please try again.');
    }
  };

  const generateCSVContent = (): string => {
    if (!dataOverview?.sample_data || dataOverview.sample_data.length === 0) {
      return 'No data available';
    }

    const headers = dataOverview.columns.join(',');
    const rows = dataOverview.sample_data.map(row => 
      Object.values(row).map(value => 
        typeof value === 'string' && value.includes(',') ? `"${value}"` : value
      ).join(',')
    );

    return [headers, ...rows].join('\n');
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

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 4 }}>
        Data Management
      </Typography>

      <Grid container spacing={3}>
        {/* Data Overview */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                <Typography variant="h6">
                  Data Overview
                </Typography>
                <Stack direction="row" spacing={2}>
                  <Button
                    variant="outlined"
                    startIcon={refreshing ? <CircularProgress size={20} /> : <Refresh />}
                    onClick={handleRefreshData}
                    disabled={refreshing}
                  >
                    {refreshing ? 'Refreshing...' : 'Refresh Data'}
                  </Button>
                  <Button
                    variant="contained"
                    startIcon={<Download />}
                    onClick={handleDownloadData}
                    sx={{
                      backgroundColor: '#FC5200',
                      '&:hover': {
                        backgroundColor: '#e64a19',
                      },
                    }}
                  >
                    Download CSV
                  </Button>
                </Stack>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Link
                  href="https://www.strava.com/athlete/training"
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

              <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary">
                      {dataOverview?.total_activities || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Activities
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary">
                      {dataOverview?.date_range.start ? 
                        new Date(dataOverview.date_range.start).getFullYear() : 
                        'N/A'
                      }
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Start Year
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary">
                      {dataOverview?.data_loaded_at ? 
                        new Date(dataOverview.data_loaded_at).toLocaleDateString() : 
                        'N/A'
                      }
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Last Updated
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>


        {/* Data Columns */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Data Fields
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Your data includes the following fields:
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap">
                {dataOverview?.columns.map((column, index) => (
                  <Chip
                    key={index}
                    label={column}
                    size="small"
                    variant="outlined"
                    sx={{ mb: 1 }}
                  />
                ))}
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Sample Data Table */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Sample Data (First 10 Records)
              </Typography>
              <TableContainer component={Paper} sx={{ backgroundColor: '#111111' }}>
                <Table>
                  <TableHead>
                    <TableRow>
                      {dataOverview?.columns.slice(0, 8).map((column, index) => (
                        <TableCell key={index} sx={{ color: '#ffffff', fontWeight: 600 }}>
                          {column}
                        </TableCell>
                      ))}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {dataOverview?.sample_data.slice(0, 10).map((row, rowIndex) => (
                      <TableRow key={rowIndex}>
                        {dataOverview.columns.slice(0, 8).map((column, colIndex) => (
                          <TableCell key={colIndex} sx={{ color: '#ffffff' }}>
                            {typeof row[column] === 'number' 
                              ? row[column].toFixed(2) 
                              : String(row[column] || '')
                            }
                          </TableCell>
                        ))}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DataPage;