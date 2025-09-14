import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StravaAuthService } from '../services/strava-auth.service';
import { StravaDataService } from '../services/strava-data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  
  dataStatus: any = null;
  isLoading = false;
  lastRefresh: string | null = null;
  
  constructor(
    private router: Router,
    private stravaAuthService: StravaAuthService,
    private stravaDataService: StravaDataService
  ) {}

  ngOnInit(): void {
    this.loadDataStatus();
  }

  navigateToAnalysis(): void {
    this.router.navigate(['/query']);
  }

  navigateToOverview(): void {
    this.router.navigate(['/overview']);
  }

  refreshUserData(): void {
    const accessToken = this.stravaAuthService.getAccessToken();
    if (!accessToken) {
      console.error('No access token available');
      return;
    }

    this.isLoading = true;
    this.stravaDataService.refreshUserData(accessToken).subscribe({
      next: (response: any) => {
        console.log('Data refreshed successfully:', response);
        this.lastRefresh = new Date().toLocaleString();
        this.loadDataStatus(); // Reload status
        this.isLoading = false;
      },
      error: (error: any) => {
        console.error('Failed to refresh data:', error);
        this.isLoading = false;
      }
    });
  }

  private loadDataStatus(): void {
    this.stravaDataService.getDataStatus().subscribe({
      next: (status: any) => {
        this.dataStatus = status;
      },
      error: (error: any) => {
        console.error('Failed to load data status:', error);
      }
    });
  }
} 