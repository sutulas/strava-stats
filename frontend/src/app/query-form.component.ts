import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { ApiService, QueryRequest, QueryResponse, ExampleQueries } from './services/api.service';

@Component({
  selector: 'app-query-form',
  templateUrl: './query-form.component.html',
  styleUrls: ['./query-form.component.css']
})
export class QueryFormComponent implements OnInit {
  @Output() resultsUpdated = new EventEmitter<{ response: any; chartUrl?: string }>();
  @Output() resultsCleared = new EventEmitter<void>();

  query: string = '';
  includeChart: boolean = true;
  isLoading: boolean = false;
  response: QueryResponse | null = null;
  error: string | null = null;
  examples: ExampleQueries | null = null;
  chartUrl: string | null = null;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadExamples();
  }

  loadExamples() {
    this.apiService.getExampleQueries().subscribe({
      next: (data) => {
        this.examples = data;
      },
      error: (err) => {
        console.error('Error loading examples:', err);
      }
    });
  }

  submitQuery() {
    if (!this.query.trim()) {
      this.error = 'Please enter a query';
      return;
    }

    this.isLoading = true;
    this.error = null;
    this.response = null;
    this.chartUrl = null;

    const request: QueryRequest = {
      query: this.query.trim(),
      include_chart: this.includeChart
    };

    this.apiService.processQuery(request).subscribe({
      next: (data) => {
        this.response = data;
        if (data.chart_generated) {
          this.chartUrl = this.apiService.getChartUrl();
        }
        this.isLoading = false;
        
        // Emit results to parent component
        this.resultsUpdated.emit({
          response: data,
          chartUrl: this.chartUrl || undefined
        });
      },
      error: (err) => {
        this.error = err.error?.detail || 'An error occurred while processing your query';
        this.isLoading = false;
      }
    });
  }

  useExample(exampleQuery: string) {
    this.query = exampleQuery;
  }

  clearResponse() {
    this.response = null;
    this.error = null;
    this.chartUrl = null;
    this.resultsCleared.emit();
  }
} 