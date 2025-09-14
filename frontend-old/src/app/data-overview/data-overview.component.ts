import { Component, OnInit } from '@angular/core';
import { ApiService, DataOverview } from '../services/api.service';

@Component({
  selector: 'app-data-overview',
  templateUrl: './data-overview.component.html',
  styleUrls: ['./data-overview.component.css']
})
export class DataOverviewComponent implements OnInit {
  dataOverview: DataOverview | null = null;
  isLoading = true;
  error: string | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadDataOverview();
  }

  loadDataOverview(): void {
    this.isLoading = true;
    this.error = null;

    this.apiService.getDataOverview().subscribe({
      next: (data) => {
        this.dataOverview = data;
        this.isLoading = false;
      },
      error: (error) => {
        this.error = error.error?.detail || 'Failed to load data overview.';
        this.isLoading = false;
      }
    });
  }
} 