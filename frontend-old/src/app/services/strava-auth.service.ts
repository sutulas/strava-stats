import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment';
import { StravaDataService } from './strava-data.service';

@Injectable({
  providedIn: 'root'
})
export class StravaAuthService {
  private readonly clientId = environment.strava.clientId;
  private readonly redirectUri = environment.strava.redirectUri;
  private readonly stravaAuthUrl = 'https://www.strava.com/oauth/authorize';

  constructor(
    private http: HttpClient,
    private router: Router,
    private stravaDataService: StravaDataService
  ) {}

  redirectToStravaAuth(): void {
    const authUrl = `${this.stravaAuthUrl}?client_id=${this.clientId}&response_type=code&redirect_uri=${this.redirectUri}&approval_prompt=force&scope=activity:read_all`;
    window.location.href = authUrl;
  }

  handleAuthCallback(code: string): Observable<any> {
    // Exchange the authorization code for tokens via backend
    return this.stravaDataService.exchangeCodeForToken(code);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('strava_access_token');
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('strava_refresh_token');
  }

  clearTokens(): void {
    localStorage.removeItem('strava_access_token');
    localStorage.removeItem('strava_refresh_token');
    localStorage.removeItem('strava_auth_code');
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  logout(): void {
    this.clearTokens();
    this.router.navigate(['/login']);
  }
} 