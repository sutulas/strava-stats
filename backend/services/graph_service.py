import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

class GraphService:
    def __init__(self):
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def graph_data(self, df):
        """
        Generate comprehensive graphs for running data analysis
        """
        # Convert start_date to datetime if it's not already
        df['start_date'] = pd.to_datetime(df['start_date'])
        
        # Create a figure with multiple subplots
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Distance over time
        plt.subplot(4, 2, 1)
        self._plot_distance_over_time(df)
        
        # 2. Pace analysis (minutes per mile)
        plt.subplot(4, 2, 2)
        self._plot_pace_analysis(df)
        
        # 3. Heart rate trends
        plt.subplot(4, 2, 3)
        self._plot_heart_rate_trends(df)
        
        # 4. Weekly mileage
        plt.subplot(4, 2, 4)
        self._plot_weekly_mileage(df)
        
        # 5. Speed vs Distance scatter
        plt.subplot(4, 2, 5)
        self._plot_speed_vs_distance(df)
        
        # 6. Suffer score analysis
        plt.subplot(4, 2, 6)
        self._plot_suffer_score_analysis(df)
        
        # 7. Monthly summary
        plt.subplot(4, 2, 7)
        self._plot_monthly_summary(df)
        
        # 8. Cadence analysis
        plt.subplot(4, 2, 8)
        self._plot_cadence_analysis(df)
        
        plt.tight_layout()
        return fig
    
    def _plot_distance_over_time(self, df):
        """Plot distance over time with trend line"""
        # Filter out invalid distances
        valid_data = df[df['distance'] > 0].copy()
        
        if len(valid_data) > 0:
            plt.scatter(valid_data['start_date'], valid_data['distance'], alpha=0.6, s=30)
            
            # Add trend line
            z = np.polyfit(range(len(valid_data)), valid_data['distance'], 1)
            p = np.poly1d(z)
            plt.plot(valid_data['start_date'], p(range(len(valid_data))), "r--", alpha=0.8)
            
            plt.title('Distance Over Time', fontsize=14, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel('Distance (miles)')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No valid distance data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Distance Over Time', fontsize=14, fontweight='bold')
    
    def _plot_pace_analysis(self, df):
        """Plot pace analysis (minutes per mile)"""
        # Calculate pace in minutes per mile, filtering out invalid data
        valid_runs = df[(df['distance'] > 0) & (df['moving_time'] > 0)].copy()
        valid_runs['pace_min_per_mile'] = valid_runs['moving_time'] / valid_runs['distance']
        
        # Filter out extreme pace values (likely GPS errors)
        valid_pace = valid_runs[(valid_runs['pace_min_per_mile'] > 3) & (valid_runs['pace_min_per_mile'] < 15)]
        
        if len(valid_pace) > 0:
            plt.hist(valid_pace['pace_min_per_mile'], bins=20, alpha=0.7, edgecolor='black')
            plt.axvline(valid_pace['pace_min_per_mile'].mean(), color='red', linestyle='--', 
                       label=f'Mean: {valid_pace["pace_min_per_mile"].mean():.1f} min/mi')
            
            plt.title('Pace Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Pace (minutes per mile)')
            plt.ylabel('Frequency')
            plt.legend()
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No valid pace data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Pace Distribution', fontsize=14, fontweight='bold')
    
    def _plot_heart_rate_trends(self, df):
        """Plot heart rate trends over time"""
        # Filter out runs with heart rate data
        hr_df = df[df['average_heartrate'] > 0].copy()
        
        if len(hr_df) > 0:
            plt.scatter(hr_df['start_date'], hr_df['average_heartrate'], 
                       alpha=0.6, s=30, label='Average HR')
            plt.scatter(hr_df['start_date'], hr_df['max_heartrate'], 
                       alpha=0.6, s=30, label='Max HR')
            
            # Add trend lines
            z_avg = np.polyfit(range(len(hr_df)), hr_df['average_heartrate'], 1)
            p_avg = np.poly1d(z_avg)
            plt.plot(hr_df['start_date'], p_avg(range(len(hr_df))), "r--", alpha=0.8)
            
            plt.title('Heart Rate Trends', fontsize=14, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel('Heart Rate (bpm)')
            plt.legend()
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No heart rate data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Heart Rate Trends', fontsize=14, fontweight='bold')
    
    def _plot_weekly_mileage(self, df):
        """Plot weekly mileage"""
        # Filter out invalid data
        valid_data = df[df['distance'] > 0].copy()
        
        if len(valid_data) > 0:
            # Group by week using a simpler approach
            valid_data['week_start'] = valid_data['start_date'].dt.to_period('W').dt.start_time
            weekly_mileage = valid_data.groupby('week_start')['distance'].sum().reset_index()
            
            if len(weekly_mileage) > 0:
                plt.bar(range(len(weekly_mileage)), weekly_mileage['distance'], alpha=0.7)
                plt.title('Weekly Mileage', fontsize=14, fontweight='bold')
                plt.xlabel('Week')
                plt.ylabel('Total Distance (miles)')
                
                # Show every 4th week label to avoid overcrowding
                if len(weekly_mileage) > 4:
                    plt.xticks(range(0, len(weekly_mileage), 4), 
                              [weekly_mileage.iloc[i]['week_start'].strftime('%m/%d') 
                               for i in range(0, len(weekly_mileage), 4)], rotation=45)
                else:
                    plt.xticks(range(len(weekly_mileage)), 
                              [weekly_mileage.iloc[i]['week_start'].strftime('%m/%d') 
                               for i in range(len(weekly_mileage))], rotation=45)
                plt.grid(True, alpha=0.3)
            else:
                plt.text(0.5, 0.5, 'No weekly data available', 
                        ha='center', va='center', transform=plt.gca().transAxes)
                plt.title('Weekly Mileage', fontsize=14, fontweight='bold')
        else:
            plt.text(0.5, 0.5, 'No valid distance data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Weekly Mileage', fontsize=14, fontweight='bold')
    
    def _plot_speed_vs_distance(self, df):
        """Plot speed vs distance scatter"""
        # Filter out invalid data
        valid_data = df[(df['distance'] > 0) & (df['average_speed'] > 0)].copy()
        
        if len(valid_data) > 0:
            plt.scatter(valid_data['distance'], valid_data['average_speed'], alpha=0.6, s=30)
            
            # Add trend line
            z = np.polyfit(valid_data['distance'], valid_data['average_speed'], 1)
            p = np.poly1d(z)
            plt.plot(valid_data['distance'], p(valid_data['distance']), "r--", alpha=0.8)
            
            plt.title('Speed vs Distance', fontsize=14, fontweight='bold')
            plt.xlabel('Distance (miles)')
            plt.ylabel('Average Speed (m/s)')
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No valid speed data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Speed vs Distance', fontsize=14, fontweight='bold')
    
    def _plot_suffer_score_analysis(self, df):
        """Plot suffer score analysis"""
        # Filter out runs with suffer score data
        suffer_df = df[df['suffer_score'] > 0].copy()
        
        if len(suffer_df) > 0:
            plt.hist(suffer_df['suffer_score'], bins=15, alpha=0.7, edgecolor='black')
            plt.axvline(suffer_df['suffer_score'].mean(), color='red', linestyle='--',
                       label=f'Mean: {suffer_df["suffer_score"].mean():.1f}')
            
            plt.title('Suffer Score Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Suffer Score')
            plt.ylabel('Frequency')
            plt.legend()
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No suffer score data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Suffer Score Distribution', fontsize=14, fontweight='bold')
    
    def _plot_monthly_summary(self, df):
        """Plot monthly summary statistics"""
        # Filter out invalid data
        valid_data = df[df['distance'] > 0].copy()
        
        if len(valid_data) > 0:
            valid_data['month'] = valid_data['start_date'].dt.to_period('M')
            monthly_stats = valid_data.groupby('month').agg({
                'distance': ['sum', 'mean', 'count'],
                'average_speed': 'mean',
                'average_heartrate': 'mean'
            }).round(2)
            
            # Flatten column names
            monthly_stats.columns = ['_'.join(col).strip() for col in monthly_stats.columns]
            
            # Plot monthly distance
            months = [str(m) for m in monthly_stats.index]
            plt.bar(range(len(months)), monthly_stats['distance_sum'], alpha=0.7)
            plt.title('Monthly Distance Summary', fontsize=14, fontweight='bold')
            plt.xlabel('Month')
            plt.ylabel('Total Distance (miles)')
            plt.xticks(range(len(months)), months, rotation=45)
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No valid distance data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Monthly Distance Summary', fontsize=14, fontweight='bold')
    
    def _plot_cadence_analysis(self, df):
        """Plot cadence analysis"""
        # Filter out runs with cadence data
        cadence_df = df[df['average_cadence'] > 0].copy()
        
        if len(cadence_df) > 0:
            plt.hist(cadence_df['average_cadence'], bins=15, alpha=0.7, edgecolor='black')
            plt.axvline(cadence_df['average_cadence'].mean(), color='red', linestyle='--',
                       label=f'Mean: {cadence_df["average_cadence"].mean():.1f} spm')
            
            plt.title('Cadence Distribution', fontsize=14, fontweight='bold')
            plt.xlabel('Average Cadence (steps per minute)')
            plt.ylabel('Frequency')
            plt.legend()
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No cadence data available', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Cadence Distribution', fontsize=14, fontweight='bold')
    
    def save_graph(self, fig, filename='running_analysis.png'):
        """Save the generated graph to a file"""
        # Create output directory if it doesn't exist
        os.makedirs('graphs', exist_ok=True)
        
        filepath = os.path.join('graphs', filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Graph saved to: {filepath}")
        return filepath
    
    def create_individual_graphs(self, df):
        """Create individual graphs for specific metrics"""
        graphs = {}
        
        # Convert start_date to datetime if it's not already
        df['start_date'] = pd.to_datetime(df['start_date'])
        
        # 1. Distance over time
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        self._plot_distance_over_time(df)
        graphs['distance_over_time'] = fig1
        
        # 2. Pace analysis
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        self._plot_pace_analysis(df)
        graphs['pace_analysis'] = fig2
        
        # 3. Heart rate trends
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        self._plot_heart_rate_trends(df)
        graphs['heart_rate_trends'] = fig3
        
        # 4. Weekly mileage
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        self._plot_weekly_mileage(df)
        graphs['weekly_mileage'] = fig4
        
        return graphs
    
    def create_weekly_mileage_line_graph(self, df, figsize=(20, 8)):
        """Create a beautiful, wide weekly mileage line graph"""
        # Convert start_date to datetime if it's not already
        df = df.copy()
        df['start_date'] = pd.to_datetime(df['start_date'])
        
        # Filter out invalid data
        valid_data = df[df['distance'] > 0].copy()
        
        if len(valid_data) == 0:
            fig, ax = plt.subplots(figsize=figsize)
            plt.text(0.5, 0.5, 'No valid distance data available', 
                    ha='center', va='center', transform=plt.gca().transAxes, fontsize=16)
            plt.title('Weekly Mileage Trend', fontsize=20, fontweight='bold', pad=20)
            return fig
        
        # Group by week using pandas period functionality
        valid_data['week_start'] = valid_data['start_date'].dt.to_period('W').dt.start_time
        weekly_mileage = valid_data.groupby('week_start')['distance'].sum().reset_index()
        weekly_mileage = weekly_mileage.sort_values('week_start')
        
        # Create the figure with custom styling
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set background color
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        
        # Create the main line plot with gradient effect
        line = ax.plot(weekly_mileage['week_start'], weekly_mileage['distance'], 
                      linewidth=3, color='#2E86AB', alpha=0.8, marker='o', 
                      markersize=6, markerfacecolor='#2E86AB', markeredgecolor='white', 
                      markeredgewidth=2)
        
        # Add area fill under the line
        ax.fill_between(weekly_mileage['week_start'], weekly_mileage['distance'], 
                       alpha=0.3, color='#2E86AB')
        
        # Add trend line
        if len(weekly_mileage) > 1:
            z = np.polyfit(range(len(weekly_mileage)), weekly_mileage['distance'], 1)
            p = np.poly1d(z)
            trend_line = p(range(len(weekly_mileage)))
            ax.plot(weekly_mileage['week_start'], trend_line, '--', 
                   color='#FF6B6B', linewidth=2, alpha=0.7, label='Trend')
        
        # Customize the plot
        ax.set_title('Weekly Mileage Trend', fontsize=24, fontweight='bold', 
                    color='#2C3E50', pad=30)
        ax.set_xlabel('Week', fontsize=16, fontweight='bold', color='#2C3E50', labelpad=15)
        ax.set_ylabel('Total Distance (miles)', fontsize=16, fontweight='bold', 
                     color='#2C3E50', labelpad=15)
        
        # Format x-axis
        ax.tick_params(axis='x', rotation=45, labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        
        # Add grid
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Add some statistics as text
        avg_mileage = weekly_mileage['distance'].mean()
        max_mileage = weekly_mileage['distance'].max()
        total_weeks = len(weekly_mileage)
        
        stats_text = f'Average: {avg_mileage:.1f} miles/week\nMax: {max_mileage:.1f} miles\nTotal Weeks: {total_weeks}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=12,
               verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
               facecolor='white', alpha=0.8, edgecolor='#2E86AB'))
        
        # Add legend if trend line exists
        if len(weekly_mileage) > 1:
            ax.legend(fontsize=12, loc='upper right')
        
        # Tight layout
        plt.tight_layout()
        
        return fig
    

if __name__ == "__main__":
    print("Graphing data...")
    graph_service = GraphService()
    
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'start_date': ['2025-01-01T10:00:00Z', '2025-01-02T10:00:00Z', '2025-01-03T10:00:00Z', '2025-01-04T10:00:00Z', '2025-01-05T10:00:00Z'],
        'start_date_local': ['2025-01-01T10:00:00Z', '2025-01-02T10:00:00Z', '2025-01-03T10:00:00Z', '2025-01-04T10:00:00Z', '2025-01-05T10:00:00Z'],
        'name': ['Morning Run', 'Evening Run', 'Long Run', 'Speed Work', 'Easy Run'],
        'distance': [3.1, 5.0, 10.0, 2.0, 4.0],
        'moving_time': [25, 40, 80, 15, 35],
        'elapsed_time': [25, 40, 80, 15, 35],
        'total_elevation_gain': [100, 200, 500, 50, 150],
        'average_speed': [8.0, 8.0, 8.0, 7.5, 8.75],
        'max_speed': [10.0, 10.0, 10.0, 9.0, 11.0],
        'average_cadence': [85, 85, 85, 90, 80],
        'average_heartrate': [150, 155, 160, 170, 145],
        'max_heartrate': [170, 175, 180, 185, 165],
        'suffer_score': [5, 7, 9, 8, 4],
        'year': [2025, 2025, 2025, 2025, 2025],
        'month': [1, 1, 1, 1, 1],
        'day': [1, 2, 3, 4, 5],
        'day_of_week': ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'time': ['10:00:00', '10:00:00', '10:00:00', '10:00:00', '10:00:00']
    })
    
    fig = graph_service.graph_data(sample_data)
    graph_service.save_graph(fig, 'running_analysis.png')
    print("Graph saved to: running_analysis.png")
    graphs = graph_service.create_individual_graphs(sample_data)
    for key, value in graphs.items():
        graph_service.save_graph(value, f"{key}.png")
        print(f"Graph saved to: {key}.png")
    