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

const TermsOfServicePage: React.FC = () => {
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
                Terms of Service
              </Typography>

              <Typography variant="body2" color="text.secondary" textAlign="center">
                Last updated: {new Date().toLocaleDateString()}
              </Typography>

              <Divider sx={{ backgroundColor: '#333333' }} />

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                1. Acceptance of Terms
              </Typography>
              <Typography variant="body1" color="text.primary">
                By accessing and using Running Stats ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </Typography>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                2. Description of Service
              </Typography>
              <Typography variant="body1" color="text.primary">
                Running Stats is an AI-powered analytics platform that:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Analyzes your Strava running data using artificial intelligence</li>
                <li>Provides personalized insights and visualizations</li>
                <li>Generates charts and graphs based on your activities</li>
                <li>Responds to natural language queries about your running data</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                3. Strava Integration
              </Typography>
              <Typography variant="body1" color="text.primary">
                This service integrates with Strava and is subject to Strava's API Agreement:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>We only access data you explicitly authorize through Strava OAuth</li>
                <li>We comply with Strava's data usage policies and restrictions</li>
                <li>We respect Strava's branding guidelines and attribution requirements</li>
                <li>We implement proper rate limiting as required by Strava</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                4. User Responsibilities
              </Typography>
              <Typography variant="body1" color="text.primary">
                As a user of this service, you agree to:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Provide accurate and complete information when registering</li>
                <li>Maintain the security of your Strava account credentials</li>
                <li>Use the service only for lawful purposes</li>
                <li>Not attempt to reverse engineer or modify the service</li>
                <li>Respect the intellectual property rights of the service</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                5. Data Usage and Privacy
              </Typography>
              <Typography variant="body1" color="text.primary">
                Your privacy is important to us. Please review our Privacy Policy, which also governs your use of the service, to understand our practices.
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>We only access your own Strava data, never other users' data</li>
                <li>Your data is cached for a maximum of 7 days as required by Strava</li>
                <li>You can request deletion of your data at any time</li>
                <li>We do not share your data with third parties</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                6. Service Availability
              </Typography>
              <Typography variant="body1" color="text.primary">
                We strive to provide reliable service, but we cannot guarantee:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Uninterrupted access to the service</li>
                <li>Error-free operation at all times</li>
                <li>Compatibility with all devices or browsers</li>
                <li>Availability of specific features or functionality</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                7. Limitation of Liability
              </Typography>
              <Typography variant="body1" color="text.primary">
                To the fullest extent permitted by law, Running Stats shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your use of the service.
              </Typography>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                8. Disclaimers
              </Typography>
              <Typography variant="body1" color="text.primary">
                The service is provided "as is" and "as available" without warranties of any kind, either express or implied, including but not limited to:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li>Warranties of merchantability, fitness for a particular purpose, or non-infringement</li>
                <li>Warranties that the service will meet your requirements</li>
                <li>Warranties that the service will be uninterrupted, timely, secure, or error-free</li>
                <li>Warranties regarding the accuracy, reliability, or completeness of the service</li>
              </Box>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                9. Third-Party Services
              </Typography>
              <Typography variant="body1" color="text.primary">
                This service integrates with third-party services including:
              </Typography>
              <Box component="ul" sx={{ pl: 3, color: 'text.primary' }}>
                <li><strong>Strava:</strong> For accessing your running data</li>
                <li><strong>OpenAI:</strong> For AI-powered analysis capabilities</li>
              </Box>
              <Typography variant="body1" color="text.primary" sx={{ mt: 2 }}>
                We are not responsible for the availability, accuracy, or content of these third-party services. Your use of these services is subject to their respective terms of service and privacy policies.
              </Typography>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                10. Termination
              </Typography>
              <Typography variant="body1" color="text.primary">
                We may terminate or suspend your access to the service immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms.
              </Typography>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                11. Changes to Terms
              </Typography>
              <Typography variant="body1" color="text.primary">
                We reserve the right to modify or replace these Terms at any time. If a revision is material, we will try to provide at least 30 days notice prior to any new terms taking effect.
              </Typography>

              <Typography variant="h6" color="primary" sx={{ fontWeight: 600 }}>
                12. Contact Information
              </Typography>
              <Typography variant="body1" color="text.primary">
                If you have any questions about these Terms of Service, please contact us:
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Email: sutulaseamu@gmail.com
                </Typography>
              </Box>

              <Divider sx={{ backgroundColor: '#333333' }} />

              <Typography variant="body2" color="text.secondary" textAlign="center">
                These terms comply with applicable laws and Strava's API Agreement requirements.
              </Typography>
            </Stack>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
};

export default TermsOfServicePage;