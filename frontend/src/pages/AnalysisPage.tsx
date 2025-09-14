import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  CircularProgress,
  Alert,
  Stack,
  Chip,
  Paper,
  Divider,
  Collapse,
  IconButton,
} from '@mui/material';
import { Send, Image, Refresh, ExpandMore, ExpandLess, Lightbulb } from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import { apiService, QueryResponse, ExampleQueries, RateLimitStatus } from '../services/apiService';

const AnalysisPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [examples, setExamples] = useState<ExampleQueries | null>(null);
  const [chartUrl, setChartUrl] = useState<string | null>(null);
  const [rateLimitStatus, setRateLimitStatus] = useState<RateLimitStatus | null>(null);
  const [showExamples, setShowExamples] = useState(false);

  useEffect(() => {
    const loadExamples = async () => {
      try {
        const examplesData = await apiService.getExampleQueries();
        setExamples(examplesData);
      } catch (err) {
        console.error('Error loading examples:', err);
      }
    };

    const loadRateLimitStatus = async () => {
      try {
        const rateLimitData = await apiService.getRateLimitStatus();
        setRateLimitStatus(rateLimitData);
      } catch (err) {
        console.error('Error loading rate limit status:', err);
      }
    };

    loadExamples();
    loadRateLimitStatus();
  }, []);

  const handleSubmit = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      setError(null);
      setResponse(null);
      setChartUrl(null);

      const result = await apiService.processQuery({
        query: query.trim(),
        include_chart: true,
      });

      setResponse(result);

      if (result.chart_generated) {
        setChartUrl(apiService.getChartUrl());
      }

      // Refresh rate limit status after successful query
      try {
        const rateLimitData = await apiService.getRateLimitStatus();
        setRateLimitStatus(rateLimitData);
      } catch (err) {
        console.error('Error refreshing rate limit status:', err);
      }
    } catch (err: any) {
      console.error('Error processing query:', err);
      
      // Handle rate limit error specifically
      if (err.response?.status === 429) {
        setError(err.response.data.detail || 'Rate limit exceeded. Please log out and log back in to reset your limit.');
        // Refresh rate limit status to show current state
        try {
          const rateLimitData = await apiService.getRateLimitStatus();
          setRateLimitStatus(rateLimitData);
        } catch (refreshErr) {
          console.error('Error refreshing rate limit status:', refreshErr);
        }
      } else {
        setError('Failed to process query. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (exampleQuery: string) => {
    setQuery(exampleQuery);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 4 }}>
        AI Analysis
      </Typography>

      <Grid container spacing={3}>
        {/* Query Input */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Ask a Question About Your Running Data
              </Typography>
              <Stack spacing={2}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="e.g., What is my average running pace? How has my performance improved over time?"
                  variant="outlined"
                  disabled={loading}
                />
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={loading || !query.trim() || (rateLimitStatus?.rate_limited ?? false)}
                    startIcon={loading ? <CircularProgress size={20} /> : <Send />}
                    sx={{
                      backgroundColor: '#ff6b35',
                      '&:hover': {
                        backgroundColor: '#e64a19',
                      },
                      '&:disabled': {
                        backgroundColor: '#666',
                        color: '#999',
                      },
                    }}
                  >
                    {loading ? 'Analyzing...' : 
                     (rateLimitStatus?.rate_limited ? 'Rate Limited' : 'Analyze')}
                  </Button>
                  <Box display="flex" flexDirection="column" alignItems="flex-end">
                    <Typography variant="body2" color="text.secondary">
                      Press Enter to submit
                    </Typography>
                    {rateLimitStatus && (
                      <Typography 
                        variant="body2" 
                        color={rateLimitStatus.rate_limited ? "error" : "text.secondary"}
                        sx={{ fontSize: '0.75rem' }}
                      >
                        Queries: {rateLimitStatus.query_count}/{rateLimitStatus.max_queries}
                        {rateLimitStatus.rate_limited && ' (Limit reached)'}
                      </Typography>
                    )}
                  </Box>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Error Display */}
        {error && (
          <Grid item xs={12}>
            <Alert severity="error">{error}</Alert>
          </Grid>
        )}

        {/* Rate Limit Warning */}
        {rateLimitStatus?.rate_limited && (
          <Grid item xs={12}>
            <Alert 
              severity="warning" 
            >
              You have reached your query limit of {rateLimitStatus.max_queries} queries.
            </Alert>
          </Grid>
        )}

        {/* Response Display - Prominent Position */}
        {response && (
          <Grid item xs={12}>
            <Card sx={{ border: '2px solid #ff6b35', backgroundColor: '#0a0a0a' }}>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <Typography variant="h5" gutterBottom sx={{ flexGrow: 1, color: '#ff6b35' }}>
                    Analysis Result
                  </Typography>
                  <Box display="flex" alignItems="center" gap={2}>
                    <Typography variant="body2" color="text.secondary">
                      Execution time: {response.execution_time.toFixed(2)}s
                    </Typography>
                    {response.chart_generated && (
                      <Chip
                        icon={<Image />}
                        label="Chart Generated"
                        color="primary"
                        variant="outlined"
                      />
                    )}
                  </Box>
                </Box>
                <Paper
                  sx={{
                    p: 3,
                    backgroundColor: '#1a1a1a',
                    border: '1px solid #333333',
                    borderRadius: 2,
                    mb: 2,
                  }}
                >
                  <ReactMarkdown
                    components={{
                      // Custom styling for markdown elements
                      p: ({ children }) => (
                        <Typography
                          variant="body1"
                          sx={{
                            lineHeight: 1.6,
                            fontSize: '1.1rem',
                            mb: 2,
                            color: '#ffffff',
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      h1: ({ children }) => (
                        <Typography
                          variant="h4"
                          sx={{
                            color: '#ff6b35',
                            mb: 2,
                            mt: 3,
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      h2: ({ children }) => (
                        <Typography
                          variant="h5"
                          sx={{
                            color: '#ff6b35',
                            mb: 2,
                            mt: 2,
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      h3: ({ children }) => (
                        <Typography
                          variant="h6"
                          sx={{
                            color: '#ff6b35',
                            mb: 1,
                            mt: 2,
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      strong: ({ children }) => (
                        <Typography
                          component="span"
                          sx={{
                            fontWeight: 'bold',
                            color: '#ff6b35',
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      em: ({ children }) => (
                        <Typography
                          component="span"
                          sx={{
                            fontStyle: 'italic',
                            color: '#cccccc',
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      ul: ({ children }) => (
                        <Box component="ul" sx={{ pl: 3, mb: 2 }}>
                          {children}
                        </Box>
                      ),
                      ol: ({ children }) => (
                        <Box component="ol" sx={{ pl: 3, mb: 2 }}>
                          {children}
                        </Box>
                      ),
                      li: ({ children }) => (
                        <Typography
                          component="li"
                          sx={{
                            color: '#ffffff',
                            mb: 0.5,
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      code: ({ children }) => (
                        <Typography
                          component="code"
                          sx={{
                            backgroundColor: '#333333',
                            color: '#ff6b35',
                            px: 1,
                            py: 0.5,
                            borderRadius: 1,
                            fontFamily: 'monospace',
                            fontSize: '0.9rem',
                          }}
                        >
                          {children}
                        </Typography>
                      ),
                      pre: ({ children }) => (
                        <Paper
                          sx={{
                            backgroundColor: '#333333',
                            p: 2,
                            mb: 2,
                            borderRadius: 1,
                            overflow: 'auto',
                          }}
                        >
                          <Typography
                            component="pre"
                            sx={{
                              color: '#ff6b35',
                              fontFamily: 'monospace',
                              fontSize: '0.9rem',
                              margin: 0,
                            }}
                          >
                            {children}
                          </Typography>
                        </Paper>
                      ),
                    }}
                  >
                    {response.response}
                  </ReactMarkdown>
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Chart Display - Right below results */}
        {chartUrl && (
          <Grid item xs={12}>
            <Card sx={{ border: '1px solid #ff6b35' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ color: '#ff6b35' }}>
                  Generated Chart
                </Typography>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    minHeight: 400,
                    backgroundColor: '#1a1a1a',
                    borderRadius: 2,
                    border: '1px solid #333333',
                  }}
                >
                  <img
                    src={chartUrl}
                    alt="Generated Chart"
                    style={{
                      maxWidth: '100%',
                      maxHeight: '100%',
                      objectFit: 'contain',
                    }}
                    onError={() => {
                      setChartUrl(null);
                    }}
                  />
                </Box>
                <Box mt={2} display="flex" justifyContent="center">
                  <Button
                    variant="outlined"
                    startIcon={<Refresh />}
                    onClick={() => setChartUrl(apiService.getChartUrl())}
                  >
                    Refresh Chart
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Example Queries - Show as collapsible after first query */}
        {examples && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box 
                  display="flex" 
                  alignItems="center" 
                  justifyContent="space-between"
                  sx={{ cursor: 'pointer' }}
                  onClick={() => setShowExamples(!showExamples)}
                >
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography variant="h6">
                      Example Queries
                    </Typography>
                  </Box>
                  <IconButton size="small">
                    {showExamples ? <ExpandLess /> : <ExpandMore />}
                  </IconButton>
                </Box>
                
                <Collapse in={showExamples}>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Try one of these example queries to explore your data:
                    </Typography>
                    <Stack spacing={2}>
                      {examples.examples.map((category, categoryIndex) => (
                        <Box key={categoryIndex}>
                          <Typography variant="subtitle1" gutterBottom>
                            {category.category}
                          </Typography>
                          <Stack direction="row" spacing={1} flexWrap="wrap">
                            {category.queries.map((exampleQuery, queryIndex) => (
                              <Chip
                                key={queryIndex}
                                label={exampleQuery}
                                onClick={() => handleExampleClick(exampleQuery)}
                                variant="outlined"
                                sx={{
                                  mb: 1,
                                  '&:hover': {
                                    backgroundColor: '#1a1a1a',
                                  },
                                }}
                              />
                            ))}
                          </Stack>
                          {categoryIndex < examples.examples.length - 1 && <Divider sx={{ mt: 2 }} />}
                        </Box>
                      ))}
                    </Stack>
                  </Box>
                </Collapse>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default AnalysisPage;