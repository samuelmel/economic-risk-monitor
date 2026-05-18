from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators import EmptyOperator
from airflow.operators import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


POSTGRES_CONN_ID = "postgres_default"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_TO_SILVER_USUARIOS_SQL = (
    PROJECT_ROOT / "scripts" / "transformations" / "raw_to_silver_usuarios.sql"
)

RAW_TO_SILVER_POSTS_SQL = (
    PROJECT_ROOT / "scripts" / "transformations" / "raw_to_silver_posts.sql"
)


default_args = {
    "owner": "samuel",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def executar_arquivo_sql(caminho_sql: Path, pre_sql: str | None = None) -> None:

    """
    Lê um arquivo SQL e executa no banco PostgreSQL.
    """

    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    if pre_sql:
        hook.run(pre_sql)

    sql = caminho_sql.read_text(encoding="utf-8")
    hook.run(sql)


def transformar_usuarios() -> None:

    """
    Executa a transformação de raw_usuarios para silver_usuarios.
    """

    executar_arquivo_sql(
        caminho_sql=RAW_TO_SILVER_USUARIOS_SQL,
        pre_sql="TRUNCATE TABLE silver_usuarios;",
    )


def transformar_posts() -> None:

    """
    Executa a transformação de raw_posts para silver_posts.
    """

    executar_arquivo_sql(
        caminho_sql=RAW_TO_SILVER_POSTS_SQL,
        pre_sql="TRUNCATE TABLE silver_posts;",
    )


with DAG (
    dag_id="etl_silver_transform",
    default_args=default_args,
    description="DAG responsável por transformar dados da camada RAW para a camada SILVER.",
    schedule_interval="30 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["silver", "transform"],
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    transform_usuarios = PythonOperator(
        task_id="transform_usuarios",
        python_callable=transformar_usuarios,
    )

    transform_posts = PythonOperator(
        task_id="transform_posts",
        python_callable=transformar_posts,
    )

    end = EmptyOperator(
        task_id="end"
    )

    start >> [transform_usuarios, transform_posts] >> end