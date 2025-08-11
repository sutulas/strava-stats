import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { StravaAuthService } from './services/strava-auth.service';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Strava Stats';
  showNavigation = false;

  constructor(
    private router: Router,
    private stravaAuthService: StravaAuthService
  ) {}

  ngOnInit(): void {
    // Listen to route changes to show/hide navigation
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.updateNavigationVisibility();
    });

    // Initial check
    this.updateNavigationVisibility();
  }

  private updateNavigationVisibility(): void {
    const currentRoute = this.router.url;
    this.showNavigation = !['/login', '/token'].includes(currentRoute) && 
                         this.stravaAuthService.isAuthenticated();
  }
} 