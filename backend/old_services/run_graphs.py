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
        
        # Generate comprehensive analysis
        print("Generating comprehensive running analysis...")
        fig = graph_service.graph_data(df)
        
        # Save the comprehensive graph
        graph_service.save_graph(fig, 'comprehensive_running_analysis.png')
        
        print("Graph generation completed successfully!")
        
        # Print some basic statistics
        print("\n=== Running Statistics ===")
        print(f"Total runs: {len(df)}")
        print(f"Total distance: {df['distance'].sum():.1f} miles")
        print(f"Average distance per run: {df['distance'].mean():.1f} miles")
        
        valid_runs = df[df['distance'] > 0]
        if len(valid_runs) > 0:
            avg_pace = valid_runs['moving_time'].sum() / valid_runs['distance'].sum()
            print(f"Average pace: {avg_pace:.1f} min/mile")
        
        if df['average_heartrate'].sum() > 0:
            hr_runs = df[df['average_heartrate'] > 0]
            print(f"Average heart rate: {hr_runs['average_heartrate'].mean():.1f} bpm")
        
        if df['suffer_score'].sum() > 0:
            suffer_runs = df[df['suffer_score'] > 0]
            print(f"Average suffer score: {suffer_runs['suffer_score'].mean():.1f}")
        
        print("\nGraphs have been saved to the 'graphs' directory!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 