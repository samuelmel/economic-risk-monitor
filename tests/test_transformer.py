import pandas as pd

from config import SILVER_DIR, GOLD_DIR


def test_silver_has_required_columns():
    df = pd.read_csv(
        SILVER_DIR / "world_bank_indicators.csv"
    )

    required_columns = {
        "country_code",
        "country_name",
        "indicator_code",
        "indicator_name",
        "year",
        "value",
    }

    assert required_columns.issubset(df.columns)


def test_year_is_numeric():
    df = pd.read_csv(
        SILVER_DIR / "world_bank_indicators.csv"
    )

    assert pd.api.types.is_numeric_dtype(df["year"])


def test_silver_has_no_duplicates():
    df = pd.read_csv(
        SILVER_DIR / "world_bank_indicators.csv"
    )

    duplicated = df.duplicated(
        subset=[
            "country_code",
            "indicator_code",
            "year",
        ]
    ).sum()

    assert duplicated == 0


def test_gold_has_required_columns():
    df = pd.read_csv(
        GOLD_DIR / "country_summary.csv"
    )

    required_columns = {
        "country_code",
        "country_name",
        "year",
        "gdp_current_usd",
        "inflation_percent",
        "unemployment_percent",
    }

    assert required_columns.issubset(df.columns)