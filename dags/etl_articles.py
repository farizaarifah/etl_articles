import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.providers.google.cloud.utils.credentials_provider import get_credentials_and_project_id
from google.cloud import bigquery

from google.cloud import storage

from datetime import timedelta, datetime, date
import psycopg2
import json
import pandas as pd
import os

start_date = datetime.now() - timedelta(hours=1)

default_args = {
    'depends_on_past': False,
    'start_date': start_date,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

schedule_interval = '0 * * * *'
dag_id = 'etl_articles'

dag = DAG (
    dag_id,
    default_args = default_args,
    schedule_interval = schedule_interval,
    user_defined_macros = dict(timedelta = timedelta)
)
    
def pull_from_postgres():
    yesterday = date.today()-timedelta(days=1)
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    conn = pg_hook.get_conn()
    cur=conn.cursor()
    cur.execute("""select * from articles where date(updated_at)={};
        """.format(yesterday))
    result=cur.fetchall()
    column_names = ['id','title','content','published_at', 'author_id', 'created_at', 'updated_at', 'deleted_at' ]

    df = pd.DataFrame(result, columns=column_names)
    print("pull from postgres success")
    df.to_csv('/tmp/articles.csv', encoding='utf-8', index=False)

# Function to transform data
def transform_articles():
    df = pd.read_csv('/tmp/articles.csv')
    
    df = df.where(df.notnull(), None)
    df['id'] = df['id'].astype(str)
    df['author_id'] = df['author_id'].astype(str)
    df['title'] = df['title'].astype(str)
    df['content'] = df['content'].astype(str)
    # convert string to timestamp
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    df['deleted_at'] = pd.to_datetime(df['deleted_at'])
    
    # Save the transformed data
    df.to_csv('/tmp/articles_transformed.csv', encoding='utf-8', index=False)

# Function to load data into BigQuery
def load_to_bigquery():
    # Use BigQueryHook to fetch the connection details
    hook = BigQueryHook(gcp_conn_id='google_cloud_default')
    credentials, project_id = hook.get_credentials_and_project_id()
    # Initialize BigQuery client
    client_bigquery = bigquery.Client(credentials=credentials, project=project_id)
    
    df = pd.read_csv('/tmp/articles_transformed.csv')
    print(df.head())
    # Replace any float representation of empty timestamps with None
    df['deleted_at'] = df['deleted_at'].apply(lambda x: None if isinstance(x, float) else x)
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
    )
    table_id= 'project_name.dataset1.articles'
    job = client_bigquery.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.

    table = client_bigquery.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )

generate_df = PythonOperator(
    task_id='pull_from_postgres',
    python_callable=pull_from_postgres,
    provide_context=True,
    dag=dag,
)

#transform
transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_articles,
    dag=dag,
)

# Create a PythonOperator to execute the print_hello function
db_to_bq_v = PythonOperator(
    task_id='db_to_bq',
    python_callable=load_to_bigquery,
    dag=dag
)

generate_df >> transform_data >> db_to_bq_v