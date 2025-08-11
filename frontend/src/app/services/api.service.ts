import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface QueryRequest {
  query: string;
  include_chart: boolean;
}

export interface QueryResponse {
  query: string;
  response: string;
  chart_generated: boolean;
  chart_url?: string;
  execution_time: number;
  timestamp: string;
  status: string;
}

export interface DataOverview {
  total_activities: number;
  date_range: {
    start: string;
    end: string;
  };
  activity_types: { [key: string]: number };
  columns: string[];
  sample_data: any[];
  data_loaded_at: string;
}

export interface ExampleQueries {
  examples: Array<{
    category: string;
    queries: string[];
  }>;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000'; // Backend URL

  constructor(private http: HttpClient) { }

  // Health check
  getHealth(): Observable<any> {
    return this.http.get(`${this.baseUrl}/health`);
  }

  // Process a query
  processQuery(request: QueryRequest): Observable<QueryResponse> {
    return this.http.post<QueryResponse>(`${this.baseUrl}/query`, request);
  }

  // Get data overview
  getDataOverview(): Observable<DataOverview> {
    return this.http.get<DataOverview>(`${this.baseUrl}/data/overview`);
  }

  // Get example queries
  getExampleQueries(): Observable<ExampleQueries> {
    return this.http.get<ExampleQueries>(`${this.baseUrl}/examples`);
  }

  // Get chart image
  getChart(): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/chart`, { responseType: 'blob' });
  }

  // Get chart as URL (for display)
  getChartUrl(): string {
    return `${this.baseUrl}/chart?t=${Date.now()}`; // Add timestamp to prevent caching
  }
} 