import duckdb
import pandas as pd

try:
    con = duckdb.connect('data/strava.duckdb', read_only=True)
    df = con.sql("SELECT * FROM fct_activities").df()
    print("Data Preview:")
    print(df.head())
    print("\nData Types:")
    print(df.dtypes)
    print("\nValue Counts for activity_type:")
    print(df['activity_type'].value_counts())
    print("\nSum of distance_km by activity_type:")
    print(df.groupby('activity_type')['distance_km'].sum())
except Exception as e:
    print(f"Error: {e}")
