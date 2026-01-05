# 🏃‍♂️ Strava API Data Pipeline & Dashboard

A production-style data engineering project that ingests Strava activity data, stores it in an S3-compatible data lake (MinIO), and transforms it into an analytics-ready warehouse using dbt and DuckDB, finally visualized in a Streamlit dashboard.

---

## 🏗️ Architecture

- **Orchestration**: Apache Airflow (Dockerized)
- **Ingestion**: Python-based Strava API integration
- **Storage**: MinIO (Raw S3 Lake) & DuckDB (Analytics Warehouse)
- **Transformation**: dbt (Data Build Tool)
- **Visualization**: Streamlit

---

## 🚀 How to Run

Follow these steps to set up the project and see your data in the dashboard.

### 1. Prerequisites
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- Python 3.9+ (for local dashboard)

### 2. Strava API Setup
1. Go to your [Strava API Settings](https://www.strava.com/settings/api).
2. Create an application if you haven't already.
3. Note your **Client ID** and **Client Secret**.

### 3. Get your Refresh Token
Strava requires an initial OAuth flow to get a long-lived refresh token.
1. Copy `.env.example` to `.env` (or create one).
2. Install dependencies: `pip install requests python-dotenv`
3. Run the helper script: 
   ```bash
   python auth_helper.py
   ```
4. Follow the instructions in the terminal to authorize the app and get your **Refresh Token**.

### 4. Configure Environment
Update your `.env` file with your credentials:
```env
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REFRESH_TOKEN=your_refresh_token
```

### 5. Launch the Infrastructure
Start the data lake (MinIO), database, and Airflow orchestration:
```bash
docker-compose up -d
```
*Wait a minute for the services to initialize.*

### 6. Run the Pipeline
1. Navigate to the Airflow UI at [http://localhost:8080](http://localhost:8080).
2. Login with `airflow` / `airflow`.
3. Locate the `strava_ingestion_dag`.
4. **Unpause** the DAG and **Trigger** it manually.
5. This will:
   - Fetch activities from Strava.
   - Save raw JSON to MinIO (`s3://raw-data`).
   - Run dbt to transform data into `data/strava.duckdb`.

### 7. View the Dashboard
Once the DAG completes successfully, run the dashboard locally:
```bash
# Install dashboard dependencies
pip install -r requirements.txt

# Launch Streamlit
streamlit run dashboard.py
```
The dashboard will open at `http://localhost:8501`.

---

## 📊 Data Models

- `stg_activities`: Cleaned staging layer reading from the raw S3 JSON.
- `fct_activities`: The final analytics table with derived metrics (km, moving time, speed).
