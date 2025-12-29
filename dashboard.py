import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

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
        fig_bar = px.bar(
            filtered_df.groupby('activity_type')['distance_km'].sum().reset_index(),
            x='activity_type',
            y='distance_km',
            color='activity_type',
            title="Total Distance per Type"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_chart_2:
        st.subheader("Activity Timeline")
        fig_line = px.scatter(
            filtered_df,
            x='start_date',
            y='distance_km',
            color='activity_type',
            size='distance_km',
            hover_data=['activity_name'],
            title="Activities Over Time"
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
    # Data Table
    st.subheader("Raw Data")
    st.dataframe(filtered_df[['start_date', 'activity_name', 'activity_type', 'distance_km', 'moving_time_minutes', 'avg_speed_kmh']])

except Exception as e:
    st.error(f"Error connecting to database or fetching data: {e}")
    st.info("Make sure the pipeline has run and 'data/strava.duckdb' exists.")
