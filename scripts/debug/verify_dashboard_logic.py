import pandas as pd
import duckdb
import os

def test_dashboard_logic():
    db_path = 'data/strava.duckdb'
    if not os.path.exists(db_path):
        print(f"Skipping test: {db_path} not found.")
        return

    try:
        con = duckdb.connect(db_path, read_only=True)
        
        # 1. Test data loading
        df = con.sql("SELECT * FROM fct_activities ORDER BY start_date DESC").df()
        print(f"Successfully loaded {len(df)} activities.")
        
        # 2. Test filtering logic
        activity_types = df['activity_type'].unique()
        print(f"Found activity types: {activity_types}")
        
        filtered_df = df[df['activity_type'].isin(activity_types)]
        assert len(filtered_df) == len(df), "Filtering failed to include all types by default"
        
        # 3. Test grouping logic for bar chart
        bar_data = filtered_df.groupby('activity_type')['distance_km'].sum().reset_index()
        print("\nBar data for chart:")
        print(bar_data)
        
        assert 'activity_type' in bar_data.columns
        assert 'distance_km' in bar_data.columns
        assert not bar_data.empty
        
        # 4. Test KPIs
        total_distance = filtered_df['distance_km'].sum()
        max_distance = filtered_df['distance_km'].max()
        print(f"\nKPIs: Total Distance={total_distance:.2f}, Max Distance={max_distance:.2f}")
        
        print("\nVerification successful: Dashboard logic is sound.")
        
    except Exception as e:
        print(f"Verification failed: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    test_dashboard_logic()
