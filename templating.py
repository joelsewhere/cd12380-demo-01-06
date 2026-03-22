import pathlib
from airflow.sdk import dag, task, Param
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

@dag(
    params={
        "event_type": Param(
            "",
            type=['string'],
            enum=[
                'Workshop',
                'Webinar',
                'Conference',
                'Bootcamp', 
                'Sprint',
                'Meetup',
                'Symposium',
                'Hackathon',
                'Summit',
                'Seminar',
                '',
                ]
            )
        }
    )
def templating():


    @task
    def read_file(path):
        
        print(path)
        print(pathlib.Path(path).read_text())


    cwd = pathlib.Path(__file__).parent
    
    path = (cwd / "{{ dag.dag_id }}/file.txt").as_posix()
    
    read_file(path)

    query = """

        SELECT * 
        FROM calendar
        LEFT JOIN events
        ON calendar.date = events.date
        WHERE calendar.date = '{{ ds }}'
        {% if params.event_type %} AND events.event_type = '{{ params.event_type }}'{% endif %}
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

    sql_op
    sql_file_op


templating()
    
