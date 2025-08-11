import { Component, Input, OnInit, OnChanges, SimpleChanges, OnDestroy, HostListener } from '@angular/core';

@Component({
  selector: 'app-weekly-pace-chart',
  templateUrl: './weekly-pace-chart.component.html',
  styleUrls: ['./weekly-pace-chart.component.css']
})
export class WeeklyPaceChartComponent implements OnInit, OnChanges, OnDestroy {
  @Input() weeklyStats: any[] = [];
  
  chartData: any[] = [];
  chartOptions: any = {};
  paceRange: { min: number; max: number } = { min: 6, max: 12 };
  
  // Tooltip properties
  showTooltip = false;
  tooltipX = 0;
  tooltipY = 0;
  tooltipData: any = null;
  private tooltipTimeout: any = null;
  private isHoveringChart = false;

  ngOnInit(): void {
    this.updateChart();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['weeklyStats']) {
      this.updateChart();
    }
  }

  ngOnDestroy(): void {
    if (this.tooltipTimeout) {
      clearTimeout(this.tooltipTimeout);
    }
  }

  @HostListener('mouseenter')
  onChartEnter(): void {
    this.isHoveringChart = true;
  }

  @HostListener('mouseleave')
  onChartLeave(): void {
    this.isHoveringChart = false;
    this.hideTooltip();
  }

  @HostListener('document:mousemove', ['$event'])
  onGlobalMouseMove(event: MouseEvent): void {
    // If we're not hovering the chart and tooltip is visible, hide it
    if (!this.isHoveringChart && this.showTooltip) {
      this.hideTooltip();
    }
  }

  private updateChart(): void {
    if (!this.weeklyStats || this.weeklyStats.length === 0) {
      this.chartData = [];
      this.paceRange = { min: 6, max: 12 };
      return;
    }

    // Process data for the chart
    this.chartData = this.weeklyStats.map(week => ({
      name: `Week of ${new Date(week.week_start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`,
      pace: week.avg_pace || 0,
      miles: week.miles || 0,
      runs: week.runs || 0
    }));

    // Update the pace range after processing the data
    this.paceRange = this.calculatePaceRange();
    
    console.log('WeeklyPaceChart - Data processed:', {
      chartData: this.chartData,
      paceRange: this.paceRange,
      weeklyStats: this.weeklyStats
    });

    // Chart configuration
    this.chartOptions = {
      series: [
        {
          name: 'Average Pace (min/mi)',
          data: this.chartData.map(item => item.pace)
        }
      ],
      chart: {
        type: 'line',
        height: 300,
        toolbar: {
          show: false
        }
      },
      xaxis: {
        categories: this.chartData.map(item => item.name),
        labels: {
          rotate: -45,
          style: {
            fontSize: '12px'
          }
        }
      },
      yaxis: {
        title: {
          text: 'Pace (min/mi)'
        },
        labels: {
          formatter: (value: number) => {
            if (value === 0) return 'N/A';
            const minutes = Math.floor(value);
            const seconds = Math.round((value - minutes) * 60);
            return `${minutes}:${seconds.toString().padStart(2, '0')}`;
          }
        }
      },
      colors: ['#f59e0b'],
      stroke: {
        curve: 'smooth',
        width: 3
      },
      markers: {
        size: 6,
        colors: ['#f59e0b'],
        strokeColors: '#ffffff',
        strokeWidth: 2
      },
      tooltip: {
        y: {
          formatter: (value: number) => {
            if (value === 0) return 'N/A';
            const minutes = Math.floor(value);
            const seconds = Math.round((value - minutes) * 60);
            return `${minutes}:${seconds.toString().padStart(2, '0')} min/mi`;
          }
        }
      },
      grid: {
        borderColor: '#e5e7eb',
        strokeDashArray: 4
      }
    };
  }

  private calculatePaceRange(): { min: number; max: number } {
    if (!this.chartData || this.chartData.length === 0) {
      return { min: 6, max: 12 }; // Default fallback
    }

    // Filter out invalid paces (0 or null)
    const validPaces = this.chartData
      .map(item => item.pace)
      .filter(pace => pace && pace > 0);

    if (validPaces.length === 0) {
      return { min: 6, max: 12 }; // Default fallback
    }

    const minPace = Math.min(...validPaces);
    const maxPace = Math.max(...validPaces);
    
    // Add some padding to the range (10% on each side)
    const range = maxPace - minPace;
    const padding = range * 0.1;
    
    // Ensure minimum range for visual appeal
    const minRange = 2; // At least 2 min/mi difference
    
    if (range < minRange) {
      const center = (minPace + maxPace) / 2;
      return {
        min: Math.max(0, center - minRange / 2),
        max: center + minRange / 2
      };
    }
    
    return {
      min: Math.max(0, minPace - padding),
      max: maxPace + padding
    };
  }

  getPaceRange(): { min: number; max: number } {
    return this.paceRange;
  }

  getChartPoints(): { x: number; y: number; data: any }[] {
    if (!this.chartData || this.chartData.length === 0) {
      return [];
    }

    const { min: minPace, max: maxPace } = this.paceRange;
    const chartWidth = 100;
    const chartHeight = 80; // Leave space for labels
    const margin = 10;

    return this.chartData.map((week, index) => {
      const x = margin + (index / (this.chartData.length - 1)) * (chartWidth - 2 * margin);
      
      let y;
      if (!week.pace || week.pace === 0) {
        y = chartHeight + margin; // Bottom of chart for invalid data
      } else {
        // Invert Y so faster paces (lower numbers) are at the top
        const normalizedPace = Math.max(minPace, Math.min(maxPace, week.pace));
        y = margin + ((maxPace - normalizedPace) / (maxPace - minPace)) * chartHeight;
      }

      return { x, y, data: week };
    });
  }

  getLinePoints(): string {
    const points = this.getChartPoints();
    if (points.length === 0) return '';

    return points.map(point => `${point.x},${point.y}`).join(' ');
  }

  getLineGradient(): string {
    const points = this.getChartPoints();
    if (points.length === 0) return '';

    // Create a linear gradient for the line
    let gradient = 'linear-gradient(to right, ';
    
    points.forEach((point, index) => {
      if (index > 0) gradient += ', ';
      gradient += `transparent ${point.x}%, #f59e0b ${point.x}%, #f59e0b ${point.x + 0.5}%`;
    });
    
    gradient += ')';
    return gradient;
  }

  onPointHover(event: MouseEvent, point: any): void {
    // Clear any existing timeout
    if (this.tooltipTimeout) {
      clearTimeout(this.tooltipTimeout);
    }
    
    this.tooltipData = point.data;
    
    // Get viewport dimensions
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    // Estimate tooltip dimensions (adjust these values based on your actual tooltip size)
    const tooltipWidth = 200;
    const tooltipHeight = 100;
    
    // Calculate initial position (10px offset from cursor)
    let x = event.clientX + 10;
    let y = event.clientY - 10;
    
    // Check if tooltip would go off the right edge
    if (x + tooltipWidth > viewportWidth) {
      x = event.clientX - tooltipWidth - 10;
    }
    
    // Check if tooltip would go off the bottom edge
    if (y + tooltipHeight > viewportHeight) {
      y = event.clientY - tooltipHeight - 10;
    }
    
    // Ensure tooltip doesn't go off the left edge
    if (x < 0) {
      x = 10;
    }
    
    // Ensure tooltip doesn't go off the top edge
    if (y < 0) {
      y = 10;
    }
    
    this.tooltipX = x;
    this.tooltipY = y;
    
    // Show tooltip after a small delay to prevent flickering
    this.tooltipTimeout = setTimeout(() => {
      this.showTooltip = true;
    }, 150);
  }

  onPointLeave(): void {
    this.hideTooltip();
  }

  private hideTooltip(): void {
    if (this.tooltipTimeout) {
      clearTimeout(this.tooltipTimeout);
      this.tooltipTimeout = null;
    }
    this.showTooltip = false;
  }

  formatPace(pace: number): string {
    if (!pace || pace === 0) return 'N/A';
    const minutes = Math.floor(pace);
    const seconds = Math.round((pace - minutes) * 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}/mi`;
  }

  formatWeekLabel(weekName: string): string {
    // Find the corresponding week data to get the actual week_start date
    const weekData = this.chartData.find(week => week.name === weekName);
    if (weekData && this.weeklyStats) {
      const originalWeek = this.weeklyStats.find(week => 
        week.avg_pace === weekData.pace && 
        week.miles === weekData.miles && 
        week.runs === weekData.runs
      );
      
      if (originalWeek && originalWeek.week_start) {
        const startDate = new Date(originalWeek.week_start);
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 6); // Add 6 days to get end of week
        
        const startMonth = startDate.toLocaleDateString('en-US', { month: 'short' });
        const startDay = startDate.getDate();
        
        if (endDate.getMonth() === startDate.getMonth()) {
          // Same month, show range
          return `${startMonth} ${startDay}-${endDate.getDate()}`;
        } else {
          // Different month, show start date
          return `${startMonth} ${startDay}`;
        }
      }
    }
    
    // Fallback to original format
    return weekName.split(' ')[2] || weekName;
  }
} 