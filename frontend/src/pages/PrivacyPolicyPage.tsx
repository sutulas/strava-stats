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
                We implement the following data retention practices:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Your Strava data is cached for a maximum of 7 days as required by Strava's API agreement</li>
                <li>Access tokens are stored temporarily and automatically expire</li>
                <li>All cached data is automatically deleted after 7 days</li>
                <li>You can request immediate deletion of your data at any time</li>
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
                6. Data Security
              </Typography>
              <Typography variant="body1" color="text.primary">
                We implement appropriate security measures to protect your data:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>All data transmission is encrypted using HTTPS</li>
                <li>Access tokens are handled securely and not logged</li>
                <li>Regular security audits and monitoring</li>
                <li>Immediate notification of any security breaches</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                7. Strava Integration
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
                8. Contact Information
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
                9. Changes to This Policy
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