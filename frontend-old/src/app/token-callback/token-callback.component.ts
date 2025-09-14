import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StravaAuthService } from '../services/strava-auth.service';
import { StravaDataService } from '../services/strava-data.service';

@Component({
  selector: 'app-token-callback',
  templateUrl: './token-callback.component.html',
  styleUrls: ['./token-callback.component.css']
})
export class TokenCallbackComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private stravaAuthService: StravaAuthService,
    private stravaDataService: StravaDataService
  ) {}

  ngOnInit(): void {
    // Get the authorization code from the URL query parameters
    this.route.queryParams.subscribe(params => {
      const code = params['code'];
      
      if (code) {
        // Handle the authorization code
        this.stravaAuthService.handleAuthCallback(code).subscribe({
          next: (response) => {
            console.log('Authentication successful:', response);
            
            // Store the tokens or user data
            if (response.access_token) {
              localStorage.setItem('strava_access_token', response.access_token);
              if (response.refresh_token) {
                localStorage.setItem('strava_refresh_token', response.refresh_token);
              }
              localStorage.setItem('strava_auth_code', code);
              
              // Automatically refresh user data
              this.refreshUserData(response.access_token);
            } else {
              console.error('No access token received');
              this.router.navigate(['/login']);
            }
          },
          error: (error) => {
            console.error('Authentication failed:', error);
            // Redirect to login page on error
            this.router.navigate(['/login']);
          }
        });
      } else {
        // No code found, redirect to login
        console.error('No authorization code found in URL');
        this.router.navigate(['/login']);
      }
    });
  }

  private refreshUserData(accessToken: string): void {
    // Call the backend to refresh user data
    this.stravaDataService.refreshUserData(accessToken).subscribe({
      next: (response) => {
        console.log('User data refreshed successfully:', response);
        // Redirect to profile page after data refresh
        this.router.navigate(['/profile']);
      },
      error: (error) => {
        console.error('Failed to refresh user data:', error);
        // Still redirect to profile page, but data might not be fresh
        this.router.navigate(['/profile']);
      }
    });
  }
} 