{{ config(materialized='view') }}

with source as (
    -- Use DuckDB's read_json_auto to read all JSON files in the bucket
    -- We use the s3:// protocol which is configured in profiles.yml
    select *
    from read_json_auto('s3://raw-data/strava/activities/*.json',
        filename=true
    )
)

select
    -- Basic casting and renaming
    id as activity_id,
    name as activity_name,
    distance as distance_meters,
    moving_time as moving_time_seconds,
    elapsed_time as elapsed_time_seconds,
    total_elevation_gain as elevation_gain_meters,
    type as activity_type,
    sport_type,
    start_date,
    start_date_local,
    average_speed,
    max_speed,
    average_heartrate,
    max_heartrate,
    filename as source_filename
from source
