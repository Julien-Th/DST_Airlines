from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='Lufthansa_API',
    tags=['Lufthansa', 'DST_Airlines'],
    schedule_interval=None,
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1)
    }
) as my_dag:

    task0 = BashOperator(
        bash_command="ls -lah /opt/airflow/dags",
        task_id="ls_dags"
    )
    task1 = BashOperator(
        bash_command="ls -lah /opt/src",
        task_id="ls_src"
    )
    task2 = BashOperator(
        bash_command="sh /opt/src/launch_flux.sh /opt /opt/src/ /opt/data/token/ /opt/data/lufthansa/",
        task_id="get_API_flux"
    )

    task0 >> task1 >> task2