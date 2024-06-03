from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'hello_world',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval='@daily',
)

# Define the Python function to be executed
def hello_world():
    print("Hello, world!")

# Define the tasks
start = DummyOperator(
    task_id='start',
    dag=dag,
)

hello_world_task = PythonOperator(
    task_id='hello_world_task',
    python_callable=hello_world,
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set the task dependencies
start >> hello_world_task >> end
