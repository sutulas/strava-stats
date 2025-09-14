import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-chart-display',
  templateUrl: './chart-display.component.html',
  styleUrls: ['./chart-display.component.css']
})
export class ChartDisplayComponent implements OnChanges {
  @Input() chartUrl: string | null = null;
  @Input() title: string = 'Generated Chart';
  
  displayUrl: string | null = null;
  
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['chartUrl'] && this.chartUrl) {
      // Construct full URL if it's a relative path
      if (this.chartUrl.startsWith('/')) {
        this.displayUrl = `http://localhost:8000${this.chartUrl}?t=${Date.now()}`;
      } else {
        this.displayUrl = `${this.chartUrl}?t=${Date.now()}`;
      }
      console.log('Chart URL:', this.chartUrl);
      console.log('Display URL:', this.displayUrl);
    } else {
      this.displayUrl = null;
    }
  }

  onImageError(event: any): void {
    console.error('Failed to load chart image:', event);
    console.error('Attempted URL:', this.displayUrl);
    // Show a fallback message
    this.displayUrl = null;
  }

  downloadChart(): void {
    if (this.displayUrl) {
      const link = document.createElement('a');
      link.href = this.displayUrl;
      link.download = 'strava-chart.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
} 