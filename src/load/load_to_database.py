import pandas as pd

from config import BASE_DIR, SILVER_DIR, GOLD_DIR
from src.load.database import Database


class DatabaseLoader:
    def __init__(self):
        self.database = Database()
        self.create_tables_sql = BASE_DIR / "sql" / "create_table.sql"

        self.silver_file = SILVER_DIR / "world_bank_indicators.csv"
        self.gold_file = GOLD_DIR / "country_summary.csv"

    def create_tables(self) -> None:
        self.database.execute_script(self.create_tables_sql)

    def load_silver(self) -> None:
        if not self.silver_file.exists():
            raise FileNotFoundError("Arquivo Silver não encontrado.")

        df = pd.read_csv(self.silver_file)

        with self.database.connect() as connection:
            df.to_sql(
                "silver_world_bank_indicators",
                connection,
                if_exists="replace",
                index=False
            )

    def load_gold(self) -> None:
        if not self.gold_file.exists():
            raise FileNotFoundError("Arquivo Gold não encontrado.")

        df = pd.read_csv(self.gold_file)

        with self.database.connect() as connection:
            df.to_sql(
                "gold_country_summary",
                connection,
                if_exists="replace",
                index=False
            )

    def run(self) -> None:
        print("Criando tabelas no banco...")
        self.create_tables()

        print("Carregando camada Silver no SQLite...")
        self.load_silver()

        print("Carregando camada Gold no SQLite...")
        self.load_gold()

        print("Banco de dados criado e carregado com sucesso.")