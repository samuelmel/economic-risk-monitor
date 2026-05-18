from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
DATABASE_DIR = DATA_DIR / "database"
LOGS_DIR = BASE_DIR / "logs"

DATABASE_PATH = DATABASE_DIR / "economic_risk.db"

COUNTRIES = {
    "BRA": "Brazil",
    "USA": "United States",
    "ARG": "Argentina",
    "DEU": "Germany",
    "CHN": "China",
}

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "FP.CPI.TOTL.ZG": "inflation_percent",
    "SL.UEM.TOTL.ZS": "unemployment_percent",
    "SP.POP.TOTL": "population_total",
}

START_YEAR = 2010
END_YEAR = 2023