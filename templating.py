from airflow.sdk import dag, task, Param
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

@dag(
        params=Param("")
)
def templating():

    @task
    def print_ds(ds):

        print(ds)


    @task
    def read_file(path):
        import pathlib

        print(pathlib.Path(path).read_text())


    query = """

        SELECT * 
        FROM calendar
        LEFT JOIN events
        ON calendar.date = events.date
        WHERE calendar.date = '{{ ds }}'

        """
    
    sql_op = SQLExecuteQueryOperator(
        task_id="sql_template",
        sql=query,
        conn_id='sqlite'
        )
    
    sql_file_op = SQLExecuteQueryOperator(
        task_id="sql_file",
        conn_id="sqlite",
        sql="sql/query.sql",
        params={
            "data": [1,2,3]
            }
        )
    
    path = "{{ dag.dag_id }}/file.txt"
    
    print_ds() >> read_file(path) >>  sql_op >> sql_file_op


templating()
    
