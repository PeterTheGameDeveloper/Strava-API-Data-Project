import duckdb
import pandas as pd

try:
    con = duckdb.connect('data/strava.duckdb', read_only=True)
    df = con.sql("SELECT * FROM fct_activities").df()
    print("Numeric column summary:")
    print(df[['distance_km', 'moving_time_minutes', 'elevation_gain_meters', 'avg_speed_kmh']].describe())
    print("\nRows with distance_km < 0:")
    print(df[df['distance_km'] < 0])
except Exception as e:
    print(f"Error: {e}")
