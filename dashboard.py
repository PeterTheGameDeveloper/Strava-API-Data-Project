import streamlit as st
import duckdb
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="Strava Activity Dashboard", layout="wide")

# Title
st.title("🏃‍♂️ Strava Activity Dashboard")

# Connect to DuckDB
@st.experimental_singleton
def get_connection():
    # Connect in read-only mode to avoid locking issues if pipeline is running
    return duckdb.connect('data/strava.duckdb', read_only=True)

try:
    con = get_connection()
    
    # Fetch Data
    df = con.sql("SELECT * FROM fct_activities ORDER BY start_date DESC").df()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    activity_types = st.sidebar.multiselect(
        "Select Activity Type",
        options=df['activity_type'].unique(),
        default=df['activity_type'].unique()
    )
    
    # Filter data
    filtered_df = df[df['activity_type'].isin(activity_types)]
    
    # KPIs
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    total_activities = len(filtered_df)
    total_distance = filtered_df['distance_km'].sum()
    total_time = filtered_df['moving_time_minutes'].sum() / 60 # hours
    max_distance = filtered_df['distance_km'].max()
    
    col1.metric("Total Activities", total_activities)
    col2.metric("Total Distance (km)", f"{total_distance:.1f}")
    col3.metric("Total Hours", f"{total_time:.1f}")
    col4.metric("Longest Activity (km)", f"{max_distance:.1f}")
    
    st.markdown("---")
    
    # Charts
    col_chart_1, col_chart_2 = st.columns(2)
    
    with col_chart_1:
        st.subheader("Distance by Activity Type")
        if not filtered_df.empty:
            # Aggregate data for bar chart
            bar_data = filtered_df.groupby('activity_type')['distance_km'].sum().reset_index()
            
            # Using st.bar_chart for better compatibility with this Streamlit version
            # It expects an index for its labels
            chart_data = bar_data.set_index('activity_type')['distance_km']
            st.bar_chart(chart_data)
        else:
            st.warning("No data available for the selected filters.")
        
    with col_chart_2:
        st.subheader("Activity Timeline")
        if not filtered_df.empty:
            # Create a clean copy and ensure numeric types
            plot_df = filtered_df.copy()
            plot_df['distance_km'] = pd.to_numeric(plot_df['distance_km'], errors='coerce')
            
            # Using Altair for the timeline as it is more robust for data-mapping
            # in older Streamlit environments
            chart = alt.Chart(plot_df).mark_circle(size=100, opacity=0.8, stroke='white', strokeWidth=0.5).encode(
                x=alt.X('start_date:T', title='Activity Date'),
                y=alt.Y('distance_km:Q', title='Distance (km)'),
                color=alt.Color('activity_type:N', title='Type'),
                tooltip=[
                    alt.Tooltip('activity_name:N', title='Activity'),
                    alt.Tooltip('start_date:T', title='Date', format='%Y-%m-%d %H:%M'),
                    alt.Tooltip('distance_km:Q', title='Distance (km)', format='.2f')
                ]
            ).properties(
                height=400
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Select activity types to view timeline.")
        
    # Data Table
    st.subheader("Raw Data")
    st.dataframe(filtered_df[['start_date', 'activity_name', 'activity_type', 'distance_km', 'moving_time_minutes', 'avg_speed_kmh']])

except Exception as e:
    st.error(f"Error connecting to database or fetching data: {e}")
    st.info("Make sure the pipeline has run and 'data/strava.duckdb' exists.")
