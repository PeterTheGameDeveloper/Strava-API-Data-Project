import duckdb
import pandas as pd

try:
    con = duckdb.connect('data/strava.duckdb', read_only=True)
    df = con.sql("SELECT * FROM fct_activities").df()
    print("Full Data Summary:")
    print(df.to_string())
except Exception as e:
    print(f"Error: {e}")
