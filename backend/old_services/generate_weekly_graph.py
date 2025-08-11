import pandas as pd
from services.graph_service import GraphService

def main():
    try:
        # Load the running data
        print("Loading running data...")
        df = pd.read_csv('fixed_formatted_run_data.csv')
        print(f"Loaded {len(df)} runs")
        
        # Initialize the graph service
        graph_service = GraphService()
        
        # Generate the beautiful weekly mileage line graph
        print("Generating beautiful weekly mileage line graph...")
        fig = graph_service.create_weekly_mileage_line_graph(df, figsize=(24, 10))
        
        # Save the graph
        graph_service.save_graph(fig, 'weekly_mileage_trend.png')
        
        print("Weekly mileage line graph generated successfully!")
        print("Graph saved as 'graphs/weekly_mileage_trend.png'")
        
        # Print some weekly statistics
        df['start_date'] = pd.to_datetime(df['start_date'])
        valid_data = df[df['distance'] > 0].copy()
        valid_data['week_start'] = valid_data['start_date'].dt.to_period('W').dt.start_time
        weekly_mileage = valid_data.groupby('week_start')['distance'].sum().reset_index()
        
        print(f"\n=== Weekly Statistics ===")
        print(f"Total weeks with runs: {len(weekly_mileage)}")
        print(f"Average weekly mileage: {weekly_mileage['distance'].mean():.1f} miles")
        print(f"Highest weekly mileage: {weekly_mileage['distance'].max():.1f} miles")
        print(f"Lowest weekly mileage: {weekly_mileage['distance'].min():.1f} miles")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 