import pandas as pd

from config import SILVER_DIR, GOLD_DIR


class SilverToGoldTransformer:
    def __init__(self):
        self.input_file = SILVER_DIR / "world_bank_indicators.csv"
        self.output_file = GOLD_DIR / "country_summary.csv"

        GOLD_DIR.mkdir(parents=True, exist_ok=True)

    def read_silver(self) -> pd.DataFrame:
        if not self.input_file.exists():
            raise FileNotFoundError(f"arquivo Silver não encontrado." 
                                    "Execute o processo de RAW para SILVER antes de rodar este processo."
                                    )
        return pd.read_csv(self.input_file)
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        # Agrupar por país e calcular a média dos indicadores
        gold = df.pivot_table(
            index=[
                "country_code",            
                "country_name",
                "year", 
            ],
            columns="indicator_name",
            values="value",
            aggfunc="first"
        ).reset_index()

        gold.columns.name = None  # Remove o nome do índice das colunas

        gold = gold.sort_values(by=["country_code", "year"])

        return gold

    def save_gold(self, df: pd.DataFrame) -> None:
        df.to_csv(self.output_file, index=False, encoding="utf-8")

    
    def run(self) -> None:
        silver_df = self.read_silver()
        gold_df = self.transform(silver_df)
        self.save_gold(gold_df)

        print(f"Transformação concluída. Arquivo Gold salvo em: {self.output_file}")
        print(f"Total de registros no arquivo Gold: {len(gold_df)}")