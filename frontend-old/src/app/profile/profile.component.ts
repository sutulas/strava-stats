import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StravaAuthService } from '../services/strava-auth.service';
import { StravaDataService } from '../services/strava-data.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  
  // User profile data
  userProfile: any = null;
  
  // User statistics and analytics
  userStats: any = null;
  
  // Recent activities
  recentActivities: any[] = [];
  
  // Data status
  dataStatus: any = null;
  
  // Loading states
  isLoadingProfile = false;
  isLoadingStats = false;
  isLoadingActivities = false;
  isLoadingDataRefresh = false;
  
  // Last refresh timestamp
  lastRefresh: string | null = null;
  
  constructor(
    private router: Router,
    private stravaAuthService: StravaAuthService,
    private stravaDataService: StravaDataService
  ) {}

  ngOnInit(): void {
    this.loadUserData();
  }

  private loadUserData(): void {
    const accessToken = this.stravaAuthService.getAccessToken();
    if (!accessToken) {
      console.error('No access token available');
      return;
    }

    // Load data status
    this.loadDataStatus();
    
    // Load user profile
    this.loadUserProfile(accessToken);
    
    // Load user stats
    this.loadUserStats(accessToken);
    
    // Load recent activities
    this.loadRecentActivities(accessToken);
  }

  private loadUserProfile(accessToken: string): void {
    this.isLoadingProfile = true;
    this.stravaDataService.getUserProfile(accessToken).subscribe({
      next: (profile: any) => {
        this.userProfile = profile;
        this.isLoadingProfile = false;
      },
      error: (error: any) => {
        console.error('Failed to load user profile:', error);
        this.isLoadingProfile = false;
      }
    });
  }

  private loadUserStats(accessToken: string): void {
    this.isLoadingStats = true;
    this.stravaDataService.getUserStats(accessToken).subscribe({
      next: (stats: any) => {
        this.userStats = stats;
        this.isLoadingStats = false;
      },
      error: (error: any) => {
        console.error('Failed to load user stats:', error);
        this.isLoadingStats = false;
      }
    });
  }

  private loadRecentActivities(accessToken: string): void {
    this.isLoadingActivities = true;
    this.stravaDataService.getRecentActivities(accessToken).subscribe({
      next: (response: any) => {
        this.recentActivities = response.activities || [];
        this.isLoadingActivities = false;
      },
      error: (error: any) => {
        console.error('Failed to load recent activities:', error);
        this.isLoadingActivities = false;
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

  refreshUserData(): void {
    const accessToken = this.stravaAuthService.getAccessToken();
    if (!accessToken) {
      console.error('No access token available');
      return;
    }

    this.isLoadingDataRefresh = true;
    this.stravaDataService.refreshUserData(accessToken).subscribe({
      next: (response: any) => {
        console.log('Data refreshed successfully:', response);
        this.lastRefresh = new Date().toLocaleString();
        this.loadDataStatus(); // Reload status
        this.loadUserStats(accessToken); // Reload stats
        this.loadRecentActivities(accessToken); // Reload activities
        this.isLoadingDataRefresh = false;
      },
      error: (error: any) => {
        console.error('Failed to refresh data:', error);
        this.isLoadingDataRefresh = false;
      }
    });
  }

  navigateToAnalysis(): void {
    this.router.navigate(['/query']);
  }

  navigateToOverview(): void {
    this.router.navigate(['/overview']);
  }

  // Helper methods for formatting
  formatPace(pace: number): string {
    if (!pace || isNaN(pace)) return 'N/A';
    const minutes = Math.floor(pace);
    const seconds = Math.round((pace - minutes) * 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}/mi`;
  }

  formatTime(minutes: number): string {
    if (!minutes || isNaN(minutes)) return 'N/A';
    const hours = Math.floor(minutes / 60);
    const mins = Math.round(minutes % 60);
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  }

  getDayOfWeekStats(day: string): any {
    if (!this.userStats?.day_of_week_stats) return null;
    return this.userStats.day_of_week_stats.find((d: any) => d.day === day) || null;
  }
} 