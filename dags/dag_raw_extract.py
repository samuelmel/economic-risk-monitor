from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators import EmptyOperator
from airflow.operators import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from src.extract_api import extract_usuarios, extract_posts


POSTGRES_CONN_ID = "postgres_default"


default_args = {
    "owner": "samuel",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def carregar_raw_usuarios() -> None:
    """
    Extrai usuários da API e carrega na tabela raw_usuarios.
    """

    df = extract_usuarios()

    if df.empty:
        raise ValueError("Nenhum usuário foi retornado pela API.")

    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = hook.get_sqlalchemy_engine()

    hook.run("TRUNCATE TABLE raw_usuarios;")

    df.to_sql(
        name="raw_usuarios",
        con=engine,
        if_exists="append",
        index=False,
    )


def carregar_raw_posts() -> None:
    """
    Extrai posts da API e carrega na tabela raw_posts.
    """
    df = extract_posts()

    if df.empty:
        raise ValueError("Nenhum post foi retornado pela API.")

    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    engine = hook.get_sqlalchemy_engine()

    hook.run("TRUNCATE TABLE raw_posts;")

    df.to_sql(
        name="raw_posts",
        con=engine,
        if_exists="append",
        index=False,
    )


with DAG(
    dag_id="etl_raw_extract",
    default_args=default_args,
    description="DAG responsável por extrair dados da API JSONPlaceholder e carregar na camada RAW.",
    schedule_interval="0 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["raw", "extract", "api"],
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    extract_usuarios_task = PythonOperator(
        task_id="extract_usuarios",
        python_callable=carregar_raw_usuarios,
    )

    extract_posts_task = PythonOperator(
        task_id="extract_posts",
        python_callable=carregar_raw_posts,
    )

    end = EmptyOperator(
        task_id="end"
    )

    start >> [extract_usuarios_task, extract_posts_task] >> end