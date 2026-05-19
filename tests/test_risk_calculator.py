import pandas as pd

from config import GOLD_DIR


def test_risk_levels_are_valid():
    df = pd.read_csv(
        GOLD_DIR / "economic_risk_score.csv"
    )

    valid_levels = {
        "Low",
        "Medium",
        "High",
    }

    assert set(df["risk_level"]).issubset(valid_levels)


def test_final_risk_score_range():
    df = pd.read_csv(
        GOLD_DIR / "economic_risk_score.csv"
    )

    assert df["final_risk_score"].between(0, 100).all()


def test_gdp_growth_exists():
    df = pd.read_csv(
        GOLD_DIR / "economic_risk_score.csv"
    )

    assert "gdp_growth_percent" in df.columns


