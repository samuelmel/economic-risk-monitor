import json
from pathlib import Path

import pandas as pd

from config import RAW_DIR, SILVER_DIR, INDICATORS


class RawToSilverTransformer:
    def __init__(self):
        self.raw_world_bank_dir = RAW_DIR / "world_bank"
        self.output_file = SILVER_DIR / "world_bank_indicators.csv"

        SILVER_DIR.mkdir(parents=True, exist_ok=True)

    def read_raw_files(self) -> list[dict]:
        rows = []

        json_files = list(self.raw_world_bank_dir.glob("*.json"))

        if not json_files:
            raise FileNotFoundError(
                "Nenhum arquivo JSON encontrado em data/raw/world_bank/. "
                "Execute primeiro a extração RAW."
            )

        for file_path in json_files:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                rows.append({
                    "country_code": item.get("countryiso3code"),
                    "country_name": item.get("country", {}).get("value"),
                    "indicator_code": item.get("indicator", {}).get("id"),
                    "indicator_original_name": item.get("indicator", {}).get("value"),
                    "year": item.get("date"),
                    "value": item.get("value"),
                    "source_file": file_path.name,
                })

        return rows

    def transform(self, rows: list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(rows)

        df["indicator_name"] = df["indicator_code"].map(INDICATORS)

        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        df = df.dropna(subset=[
            "country_code",
            "country_name",
            "indicator_code",
            "indicator_name",
            "year",
            "value",
        ])

        df["year"] = df["year"].astype(int)

        df = df.drop_duplicates(
            subset=["country_code", "indicator_code", "year"]
        )

        df = df[
            [
                "country_code",
                "country_name",
                "indicator_code",
                "indicator_name",
                "year",
                "value",
                "source_file",
            ]
        ]

        df = df.sort_values(
            by=["country_code", "indicator_code", "year"]
        )

        return df

    def save_silver(self, df: pd.DataFrame) -> None:
        df.to_csv(self.output_file, index=False, encoding="utf-8")

    def run(self) -> None:
        print("Iniciando transformação RAW → SILVER...")

        rows = self.read_raw_files()
        df = self.transform(rows)
        self.save_silver(df)

        print(f"Silver criado com sucesso: {self.output_file}")
        print(f"Total de registros: {len(df)}")