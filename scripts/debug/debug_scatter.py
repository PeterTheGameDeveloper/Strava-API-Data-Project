import pandas as pd
import duckdb
import plotly.express as px

def debug_scatter_values():
    con = duckdb.connect('data/strava.duckdb', read_only=True)
    df = con.sql("SELECT * FROM fct_activities ORDER BY start_date DESC").df()
    
    print("DataFrame Info:")
    print(df.info())
    print("\nDataFrame Values (First 15):")
    print(df[['start_date', 'activity_name', 'activity_type', 'distance_km']].to_string())
    
    # Simulate filtering
    activity_types = df['activity_type'].unique()
    filtered_df = df[df['activity_type'].isin(activity_types)]
    
    print("\nFiltered DataFrame Distance Stats:")
    print(filtered_df['distance_km'].describe())
    
    # Check if there are any duplicate names or weird types
    print("\nDistance KM Type:", type(filtered_df['distance_km'].iloc[0]))
    
    # Try creating the plotly figure and inspect data
    fig = px.scatter(
        filtered_df,
        x='start_date',
        y='distance_km',
        color='activity_type'
    )
    
    print("\nPlotly Trace Data (y values):")
    for trace in fig.data:
        print(f"Trace {trace.name}: {trace.y}")

if __name__ == "__main__":
    debug_scatter_values()
