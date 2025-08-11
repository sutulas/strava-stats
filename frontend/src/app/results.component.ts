import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent {
  @Input() response: any;
  @Input() chartUrl: string | null = null;
  @Output() clearResults = new EventEmitter<void>();

  onClearResults() {
    this.clearResults.emit();
  }
} 