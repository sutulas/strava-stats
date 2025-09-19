import React from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Stack,
  Divider,
} from '@mui/material';
import { ArrowBack } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';

const PrivacyPolicyPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        backgroundColor: '#000000',
        padding: 3,
      }}
    >
      <Container maxWidth="md">
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate(-1)}
          sx={{
            color: '#FC5200',
            mb: 3,
            '&:hover': {
              backgroundColor: 'rgba(252, 82, 0, 0.1)',
            },
          }}
        >
          Back
        </Button>

        <Card
          sx={{
            backgroundColor: '#111111',
            border: '1px solid #333333',
            borderRadius: 3,
          }}
        >
          <CardContent sx={{ padding: 4 }}>
            <Stack spacing={3}>
              <Typography
                variant="h3"
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
                Privacy Policy
              </Typography>

              <Typography variant="body2" color="text.secondary" textAlign="center">
                Last updated: {new Date().toLocaleDateString()}
              </Typography>

              <Divider sx={{ backgroundColor: '#333333' }} />

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                1. Information We Collect
              </Typography>
              <Typography variant="body1" color="text.primary">
                We collect and process the following information from your Strava account:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Your Strava profile information (name, username, location)</li>
                <li>Your running activity data (distance, time, pace, heart rate, etc.)</li>
                <li>Activity metadata (dates, routes, elevation data)</li>
                <li>Your Strava access token (temporarily stored for API access)</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                2. How We Use Your Information
              </Typography>
              <Typography variant="body1" color="text.primary">
                We use your information exclusively to:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Provide AI-powered analysis of your running data</li>
                <li>Generate personalized insights and visualizations</li>
                <li>Create charts and graphs based on your activities</li>
                <li>Respond to your natural language queries about your running data</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                3. Data Storage and Retention
              </Typography>
              <Typography variant="body1" color="text.primary">
                We implement the following data storage and retention practices:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li><strong>Primary Storage:</strong> Your processed Strava data is stored securely in Supabase (PostgreSQL database)</li>
                <li><strong>Data Persistence:</strong> Data persists across sessions to provide faster access and better user experience</li>
                <li><strong>Data Format:</strong> Your running activities are stored as processed, anonymized data (no personal identifiers)</li>
                <li><strong>User Identification:</strong> Data is linked only to your Strava user ID (numeric identifier)</li>
                <li><strong>Retention Period:</strong> Data is retained until you request deletion or revoke Strava access</li>
                <li><strong>Automatic Cleanup:</strong> You can request immediate deletion of your data at any time</li>
                <li><strong>Cache Management:</strong> API response caches are stored temporarily for performance optimization</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                4. Data Sharing and Disclosure
              </Typography>
              <Typography variant="body1" color="text.primary">
                We do not share, sell, or disclose your personal data to third parties. Your data is:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Only accessible to you through your authenticated session</li>
                <li>Not shared with other users or third parties</li>
                <li>Not used for advertising or marketing purposes</li>
                <li>Not sold to data brokers or advertisers</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                5. Your Rights and Choices
              </Typography>
              <Typography variant="body1" color="text.primary">
                You have the following rights regarding your data:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li><strong>Access:</strong> View all data we have collected about you</li>
                <li><strong>Deletion:</strong> Request complete deletion of your data</li>
                <li><strong>Withdrawal:</strong> Revoke access to your Strava account at any time</li>
                <li><strong>Portability:</strong> Export your data in a readable format</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                6. Third-Party Services
              </Typography>
              <Typography variant="body1" color="text.primary">
                We use the following third-party services to provide our functionality:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li><strong>Supabase:</strong> PostgreSQL database service for secure data storage and management</li>
                <li><strong>Strava API:</strong> For accessing your running activity data</li>
                <li><strong>OpenAI API:</strong> For AI-powered analysis and natural language processing</li>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                These services are GDPR-compliant and maintain high security standards. We do not share your personal data with any other third parties.
              </Typography>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                7. Data Security
              </Typography>
              <Typography variant="body1" color="text.primary">
                We implement appropriate security measures to protect your data:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>All data transmission is encrypted using HTTPS/TLS</li>
                <li>Database connections are encrypted and secured</li>
                <li>Access tokens are handled securely and not logged</li>
                <li>User data is isolated by user ID with proper access controls</li>
                <li>Regular security audits and monitoring</li>
                <li>Immediate notification of any security breaches</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                8. Strava Integration
              </Typography>
              <Typography variant="body1" color="text.primary">
                This application integrates with Strava and complies with Strava's API Agreement:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>We only access data you explicitly authorize</li>
                <li>We respect Strava's data usage policies</li>
                <li>We display proper Strava attribution and branding</li>
                <li>We comply with Strava's rate limiting requirements</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                9. Contact Information
              </Typography>
              <Typography variant="body1" color="text.primary">
                If you have questions about this privacy policy or want to exercise your rights, please contact us:
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Email: sutulaseamu@gmail.com
                </Typography>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                10. Changes to This Policy
              </Typography>
              <Typography variant="body1" color="text.primary">
                We may update this privacy policy from time to time.
              </Typography>

              <Divider sx={{ backgroundColor: '#333333' }} />

              <Typography variant="body2" color="text.secondary" textAlign="center">
                This privacy policy complies with GDPR, UK GDPR, and Strava's API Agreement requirements.
              </Typography>
            </Stack>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
};

export default PrivacyPolicyPage;