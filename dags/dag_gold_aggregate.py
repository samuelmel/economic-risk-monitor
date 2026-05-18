from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


POSTGRES_CONN_ID = "postgres_default"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SILVER_TO_GOLD_METRICAS_SQL = (
    PROJECT_ROOT / "scripts" / "transformations" / "silver_to_gold_metricas.sql"
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


def criar_metricas_usuario() -> None:
    """
    Executa a agregação da camada SILVER para a camada GOLD.
    """
    executar_arquivo_sql(
        caminho_sql=SILVER_TO_GOLD_METRICAS_SQL,
        pre_sql="TRUNCATE TABLE gold_metricas_usuario;",
    )


with DAG(
    dag_id="etl_gold_aggregate",
    default_args=default_args,
    description="DAG responsável por criar métricas agregadas na camada GOLD.",
    schedule="0 7 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["gold", "aggregate", "analytics"],
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    create_metricas_usuario = PythonOperator(
        task_id="create_metricas_usuario",
        python_callable=criar_metricas_usuario,
    )

    end = EmptyOperator(
        task_id="end"
    )

    start >> create_metricas_usuario >> end