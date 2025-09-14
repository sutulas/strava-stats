import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService, QueryResponse } from '../services/api.service';

@Component({
  selector: 'app-query-form',
  templateUrl: './query-form.component.html',
  styleUrls: ['./query-form.component.css']
})
export class QueryFormComponent {
  queryForm: FormGroup;
  isLoading = false;
  error: string | null = null;
  currentResponse: QueryResponse | null = null;
  examples = [
    "What is my average running pace?",
    "How many miles have I run this year?",
    "Show me my weekly mileage trends",
    "Create a chart of my distance over time",
    "What is my fastest run?",
    "Show me my total elevation gain"
  ];

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {
    this.queryForm = this.fb.group({
      query: ['', [Validators.required, Validators.minLength(3)]],
      includeChart: [true]
    });
  }

  onSubmit(): void {
    if (this.queryForm.valid) {
      this.isLoading = true;
      this.error = null;
      this.currentResponse = null;

      const formData = this.queryForm.value;
      
      this.apiService.processQuery({
        query: formData.query,
        include_chart: formData.includeChart
      }).subscribe({
        next: (response) => {
          this.isLoading = false;
          this.currentResponse = response;
          console.log('API Response:', response);
          console.log('Chart generated:', response.chart_generated);
          console.log('Chart URL:', response.chart_url);
        },
        error: (error) => {
          this.isLoading = false;
          this.error = error.error?.detail || 'An error occurred while processing your query.';
          console.error('API Error:', error);
        }
      });
    }
  }

  useExample(example: string): void {
    this.queryForm.patchValue({ query: example });
  }

  clearResults(): void {
    this.currentResponse = null;
    this.queryForm.reset({ includeChart: true });
    this.error = null;
  }

  get chartUrl(): string | null {
    if (this.currentResponse?.chart_generated && this.currentResponse?.chart_url) {
      return this.currentResponse.chart_url;
    }
    return null;
  }
} 