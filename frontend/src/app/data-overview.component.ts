import { Component, OnInit } from '@angular/core';
import { ApiService, DataOverview } from './services/api.service';

@Component({
  selector: 'app-data-overview',
  templateUrl: './data-overview.component.html',
  styleUrls: ['./data-overview.component.css']
})
export class DataOverviewComponent implements OnInit {
  dataOverview: DataOverview | null = null;
  isLoading: boolean = true;
  error: string | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadDataOverview();
  }

  loadDataOverview() {
    this.isLoading = true;
    this.error = null;

    this.apiService.getDataOverview().subscribe({
      next: (data: DataOverview) => {
        this.dataOverview = data;
        this.isLoading = false;
      },
      error: (err: any) => {
        this.error = err.error?.detail || 'Failed to load data overview';
        this.isLoading = false;
      }
    });
  }

  refreshData() {
    this.loadDataOverview();
  }

  getActivityTypesKeys(): string[] {
    if (this.dataOverview?.activity_types) {
      return Object.keys(this.dataOverview.activity_types);
    }
    return [];
  }

  getMaxActivityCount(): number {
    if (this.dataOverview?.activity_types) {
      return Math.max(...Object.values(this.dataOverview.activity_types));
    }
    return 1;
  }
} 