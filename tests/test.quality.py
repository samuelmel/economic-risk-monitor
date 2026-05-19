
import pandas as pd
from config import SILVER_DIR, GOLD_DIR


def test_silver_file_exists():
    assert (
        SILVER_DIR / "world_bank_indicators.csv"
    ).exists()


def test_gold_file_exists():
    assert (
        GOLD_DIR / "country_summary.csv"
    ).exists()



def test_silver_has_no_null_country_code():
    df = pd.read_csv(
        SILVER_DIR / "world_bank_indicators.csv"
    )

    assert df["country_code"].isnull().sum() == 0


def test_year_range():
    df = pd.read_csv(
        SILVER_DIR / "world_bank_indicators.csv"
    )

    assert df["year"].min() >= 2010
    assert df["year"].max() <= 2023