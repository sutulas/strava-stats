import { Component, Input, Output, EventEmitter } from '@angular/core';
import { QueryResponse } from '../services/api.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent {
  @Input() response: QueryResponse | null = null;
  @Output() clearResults = new EventEmitter<void>();

  get chartUrl(): string | null {
    if (this.response?.chart_generated && this.response?.chart_url) {
      return this.response.chart_url;
    }
    return null;
  }

  onClearResults(): void {
    this.clearResults.emit();
  }
} 