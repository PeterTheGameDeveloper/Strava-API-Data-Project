from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import json
import os
import sys

# Add include directory to path to import strava_client
sys.path.append('/opt/airflow/include')
from strava_client import StravaClient

# S3 Wrapper using s3fs for simplicity in the tailored environment or Airflow Hook
# We will use simple s3fs for writing JSONs to MinIO.
import s3fs

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_and_stage_strava_data(**context):
    """
    Fetches data from Strava and writes it to MinIO (S3).
    """
    # Load credentials from Environment or Airflow Variables
    # For this project, we assume environment variables are passed to Docker
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Strava credentials not found in environment variables.")

    client = StravaClient(client_id, client_secret, refresh_token)
    
    # Determine the 'after' timestamp for incremental load
    # For now, simplistic approach: last 3 days
    # Real production: use Airflow Variable to store last high-watermark
    days_back = 3
    after_timestamp = int((datetime.now() - timedelta(days=days_back)).timestamp())
    
    print(f"Fetching activities since {datetime.fromtimestamp(after_timestamp)}")
    activities = client.get_activities(after_timestamp=after_timestamp)
    
    if not activities:
        print("No new activities found.")
        return

    # Write to MinIO
    # Execution Date for partitioning
    execution_date = context['ds']
    
    # Initialize S3 filesystem (connects to MinIO container)
    s3 = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'http://minio:9000'},
        key='minioadmin',
        secret='minioadmin'
    )
    
    file_path = f"s3://raw-data/strava/activities/{execution_date}.json"
    
    with s3.open(file_path, 'w') as f:
        json.dump(activities, f)
        
    print(f"Successfully wrote {len(activities)} activities to {file_path}")

with DAG(
    'strava_ingestion_dag',
    default_args=default_args,
    description='Ingests Strava activities to S3(MinIO)',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['ingestion', 'strava'],
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_strava_activities',
        python_callable=fetch_and_stage_strava_data,
        provide_context=True
    )

    transform_task = BashOperator(
        task_id='transform_data',
        bash_command='cd /opt/airflow/dbt_project && dbt build --profiles-dir .',
        env={
            'dbt_s3_endpoint': 'minio:9000',
            'dbt_s3_access_key': 'minioadmin',
            'dbt_s3_secret_key': 'minioadmin',
        },
        append_env=True
    )

    ingest_task >> transform_task
