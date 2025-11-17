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
      // Download all data from the API
      const blob = await apiService.downloadAllData();
      
      // Create download link
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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4" component="h1">
          Data Management
        </Typography>
        <Stack 
          direction={{ xs: 'column', sm: 'row' }} 
          spacing={1.5}
          sx={{ 
            alignItems: { xs: 'stretch', sm: 'center' }
          }}
        >
          <Button
            variant="outlined"
            size="small"
            startIcon={refreshing ? <CircularProgress size={16} /> : <Refresh />}
            onClick={handleRefreshData}
            disabled={refreshing}
            sx={{ 
              minWidth: { xs: '100%', sm: 'auto' },
              fontSize: '0.875rem'
            }}
          >
            {refreshing ? 'Refreshing...' : 'Refresh Data'}
          </Button>
          <Button
            variant="contained"
            size="small"
            startIcon={<Download />}
            onClick={handleDownloadData}
            sx={{
              backgroundColor: '#FC5200',
              minWidth: { xs: '100%', sm: 'auto' },
              fontSize: '0.875rem',
              '&:hover': {
                backgroundColor: '#e64a19',
              },
            }}
          >
            Download CSV
          </Button>
        </Stack>
      </Box>

      <Grid container spacing={2}>
        {/* Data Overview Stats */}
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" color="primary" sx={{ fontSize: '1.75rem', mb: 0.5 }}>
                {dataOverview?.total_activities || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                Total Activities
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" color="primary" sx={{ fontSize: '1.75rem', mb: 0.5 }}>
                {dataOverview?.date_range.start ? 
                  new Date(dataOverview.date_range.start).getFullYear() : 
                  'N/A'
                }
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                Start Year
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" color="primary" sx={{ fontSize: '1.75rem', mb: 0.5 }}>
                {dataOverview?.date_range.end ? 
                  new Date(dataOverview.date_range.end).getFullYear() : 
                  'N/A'
                }
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                End Year
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" color="primary" sx={{ fontSize: '1.5rem', mb: 0.5 }}>
                {dataOverview?.data_loaded_at ? 
                  new Date(dataOverview.data_loaded_at).toLocaleDateString() : 
                  'N/A'
                }
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                Last Updated
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Data Columns */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1.5 }}>
                Data Fields
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph sx={{ fontSize: '0.875rem', mb: 1.5 }}>
                Your data includes the following fields:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {dataOverview?.columns.map((column, index) => (
                  <Chip
                    key={index}
                    label={column}
                    size="small"
                    variant="outlined"
                    sx={{ 
                      fontSize: '0.75rem',
                      height: '24px'
                    }}
                  />
                ))}
              </Box>
              <Box sx={{ mt: 2 }}>
                <Link
                  href="https://www.strava.com/athlete/training"
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{
                    color: '#FC5200',
                    textDecoration: 'underline',
                    fontWeight: 'bold',
                    fontSize: '0.8rem',
                  }}
                >
                  View on Strava →
                </Link>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Sample Data Table */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
              <Typography variant="h6" gutterBottom sx={{ fontSize: '1rem', mb: 1.5 }}>
                Sample Data (First 3 Records)
              </Typography>
              <TableContainer 
                component={Paper} 
                sx={{ 
                  backgroundColor: '#111111',
                  maxHeight: 400,
                  overflow: 'auto',
                  '&::-webkit-scrollbar': {
                    width: '8px',
                    height: '8px',
                  },
                  '&::-webkit-scrollbar-track': {
                    backgroundColor: '#1a1a1a',
                  },
                  '&::-webkit-scrollbar-thumb': {
                    backgroundColor: '#333333',
                    borderRadius: '4px',
                    '&:hover': {
                      backgroundColor: '#444444',
                    },
                  },
                }}
              >
                <Table size="small" stickyHeader>
                  <TableHead>
                    <TableRow>
                      {dataOverview?.columns.slice(0, 8).map((column, index) => (
                        <TableCell 
                          key={index} 
                          sx={{ 
                            color: '#ffffff', 
                            fontWeight: 600,
                            backgroundColor: '#1a1a1a',
                            fontSize: '0.75rem',
                            py: 1,
                            borderBottom: '1px solid #333333'
                          }}
                        >
                          {column}
                        </TableCell>
                      ))}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {dataOverview?.sample_data.slice(0, 10).map((row, rowIndex) => (
                      <TableRow 
                        key={rowIndex}
                        sx={{
                          '&:hover': {
                            backgroundColor: '#1a1a1a',
                          },
                          '&:nth-of-type(even)': {
                            backgroundColor: '#0f0f0f',
                          },
                        }}
                      >
                        {dataOverview.columns.slice(0, 8).map((column, colIndex) => (
                          <TableCell 
                            key={colIndex} 
                            sx={{ 
                              color: '#ffffff',
                              fontSize: '0.75rem',
                              py: 0.75,
                              borderBottom: '1px solid #1a1a1a'
                            }}
                          >
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