{{ config(materialized='table') }}

with staging as (
    select * from {{ ref('stg_activities') }}
)

select
    activity_id,
    activity_name,
    activity_type,
    start_date,
    
    -- derived metrics
    distance_meters / 1000.0 as distance_km,
    moving_time_seconds / 60.0 as moving_time_minutes,
    elevation_gain_meters,
    
    -- simple speed calc (km/h)
    (distance_meters / 1000.0) / (moving_time_seconds / 3600.0) as avg_speed_kmh,
    
    source_filename
from staging
