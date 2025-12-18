import duckdb

# Connect to the database file
con = duckdb.connect('data/strava.duckdb')

# Query the final table
df = con.sql("SELECT * FROM fct_activities").df()
print(df.head())