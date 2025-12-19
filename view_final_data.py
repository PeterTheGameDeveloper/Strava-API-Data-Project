import duckdb

# Connect to the database file
con = duckdb.connect('data/strava.duckdb')

# Query the final table
df = con.sql("SELECT * FROM fct_activities").df()
print(df.head())

# Save to JSON
df.to_json('data/final_data.json', orient='records', indent=4, date_format='iso')
print("\nData saved to data/final_data.json")