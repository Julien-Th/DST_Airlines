from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
import datetime

my_dag = DAG(
    dag_id='my_very_first_dag',
    description='My first DAG created with DataScientest',
    tags=['tutorial', 'datascientest'],
    schedule_interval=None,
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(2),
    }
)

# definition of the function to execute
def print_date_and_hello():
    print(datetime.datetime.now())
    print('Hello from Airflow')


my_task = PythonOperator(
    task_id='my_very_first_task',
    python_callable=print_date_and_hello,
    dag=my_dag
)