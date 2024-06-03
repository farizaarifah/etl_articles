from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
import pandas as pd

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'select_from_bigquery',
    default_args=default_args,
    description='A simple DAG to select data from BigQuery',
    schedule_interval='@daily',
)

# Define the SQL query
SQL_QUERY = """
SELECT
*
FROM
`fresh-ward-335203.dataset1.kumparan_articles`
"""

# Define the Python function to process the results
def process_bq_results():
    bq_hook = BigQueryHook(bigquery_conn_id='google_cloud_default', use_legacy_sql=False)
    df = bq_hook.get_pandas_df(SQL_QUERY)
    # Process the DataFrame (e.g., print it, save it to a file, etc.)
    print(df.head())


select_from_bq = PythonOperator(
    task_id='select_from_bq',
    python_callable=process_bq_results,
    dag=dag,
)

print_hello = BashOperator(
    task_id='print_hello',
    bash_command='pwd',
    dag=dag,
)
