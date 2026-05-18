import json
from datetime import datetime
from pathlib import Path

import requests

from config import COUNTRIES, INDICATORS, START_YEAR, END_YEAR, RAW_DIR


class WorldBankExtractor:
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        self.output_dir = RAW_DIR / "world_bank"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_indicator(self, country_code: str, indicator_code: str) -> list[dict]:
        url = self.base_url.format(
            country=country_code,
            indicator=indicator_code
        )

        params = {
            "format": "json",
            "date": f"{START_YEAR}:{END_YEAR}",
            "per_page": 1000,
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if len(data) < 2 or data[1] is None:
            return []

        return data[1]

    def save_raw_json(
        self,
        data: list[dict],
        country_code: str,
        indicator_code: str
    ) -> None:
        extraction_date = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_name = (
            f"{country_code}_{indicator_code}_"
            f"{START_YEAR}_{END_YEAR}_{extraction_date}.json"
        )

        file_path = self.output_dir / file_name

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def extract_all(self) -> None:
        for country_code in COUNTRIES:
            for indicator_code in INDICATORS:
                print(f"Extraindo {country_code} - {indicator_code}")

                data = self.fetch_indicator(country_code, indicator_code)

                if data:
                    self.save_raw_json(
                        data=data,
                        country_code=country_code,
                        indicator_code=indicator_code
                    )
                    print("Salvo com sucesso.")
                else:
                    print("Nenhum dado encontrado.")