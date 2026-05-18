import pandas as pd

from config import GOLD_DIR

class EconomicRiskScore:
    def __init__(self):
        self.input_file = GOLD_DIR / "country_summary.csv"
        self.output_file = GOLD_DIR / "economic_risk_score.csv"

    def read_gold(self) -> pd.DataFrame:
        if not self.input_file.exists():
            raise FileNotFoundError(
                "Arquivo Gold não encontrado. Execute primeiro SILVER → GOLD."
            )

        return pd.read_csv(self.input_file)

    def calculate_gdp_growth(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values(["country_code", "year"]).copy()

        df["gdp_growth_percent"] = (
            df.groupby("country_code")["gdp_current_usd"]
            .pct_change() * 100
        )

        return df

    def normalize_score(self, series: pd.Series, higher_is_worse: bool = True) -> pd.Series:
        min_value = series.min()
        max_value = series.max()

        if min_value == max_value:
            return pd.Series([0] * len(series), index=series.index)

        normalized = ((series - min_value) / (max_value - min_value)) * 100

        if higher_is_worse:
            return normalized

        return 100 - normalized

    def classify_risk(self, score: float) -> str:
        if score <= 30:
            return "Low"

        if score <= 60:
            return "Medium"

        return "High"

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.calculate_gdp_growth(df)

        df["inflation_score"] = self.normalize_score(
            df["inflation_percent"],
            higher_is_worse=True
        )

        df["unemployment_score"] = self.normalize_score(
            df["unemployment_percent"],
            higher_is_worse=True
        )

        df["gdp_growth_score"] = self.normalize_score(
            df["gdp_growth_percent"],
            higher_is_worse=False
        )

        df["final_risk_score"] = (
            df["inflation_score"] * 0.4
            + df["unemployment_score"] * 0.3
            + df["gdp_growth_score"] * 0.3
        )

        df["risk_level"] = df["final_risk_score"].apply(self.classify_risk)

        output_columns = [
            "country_code",
            "country_name",
            "year",
            "inflation_percent",
            "unemployment_percent",
            "gdp_growth_percent",
            "inflation_score",
            "unemployment_score",
            "gdp_growth_score",
            "final_risk_score",
            "risk_level",
        ]

        df = df[output_columns]

        df = df.dropna(subset=[
            "inflation_percent",
            "unemployment_percent",
            "gdp_growth_percent",
            "final_risk_score",
        ])

        return df

    def save_score(self, df: pd.DataFrame) -> None:
        df.to_csv(self.output_file, index=False, encoding="utf-8")

    def run(self) -> None:
        print("Calculando score de risco econômico...")

        gold_df = self.read_gold()
        score_df = self.transform(gold_df)
        self.save_score(score_df)

        print(f"Score salvo em: {self.output_file}")
        print(f"Total de registros no score: {len(score_df)}")