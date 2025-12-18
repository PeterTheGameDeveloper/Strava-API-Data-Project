# Strava API Data Pipeline

A production-style ETL pipeline that ingests Strava activity data, stores it in an S3-compatible data lake, and transforms it into an analytics-ready warehouse using dbt and DuckDB.

## Architecture

- **Ingestion**: Python (Airflow) -> MinIO (S3)
- **Transformation**: dbt -> DuckDB
- **Orchestration**: Apache Airflow (Docker)
- **Storage**: MinIO (Raw), DuckDB (Warehouse)

## Setup

1. **Prerequisites**: Docker & Docker Compose.
2. **Environment**:
   Copy `.env.example` to `.env` and add your Strava API keys.
   ```
   STRAVA_CLIENT_ID=...
   STRAVA_CLIENT_SECRET=...
   STRAVA_REFRESH_TOKEN=...
   ```
3. **Run**:
   ```bash
   docker-compose up -d
   ```
4. **Airflow**: Navigate to `http://localhost:8080` (airflow/airflow).

## Models

- `stg_activities`: View over raw JSON files in S3.
- `fct_activities`: Verified analytics table with derived metrics.
