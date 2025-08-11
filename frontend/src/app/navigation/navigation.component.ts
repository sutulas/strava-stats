import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { StravaAuthService } from '../services/strava-auth.service';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent {
  navItems = [
    { path: '/profile', label: 'Profile' },
    { path: '/query', label: 'Analysis' },
    { path: '/overview', label: 'Data Overview' },
  ];

  constructor(
    private router: Router,
    private stravaAuthService: StravaAuthService
  ) {}

  logout(): void {
    this.stravaAuthService.clearTokens();
    this.router.navigate(['/login']);
  }
} 