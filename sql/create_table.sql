CREATE TABLE IF NOT EXISTS silver_world_bank_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT NOT NULL,
    country_name TEXT NOT NULL,
    indicator_name TEXT NOT NULL,
    indicator_code TEXT NOT NULL,
    year INT NOT NULL,
    value REAL NOT NULL,
    source_file TEXT
);

CREATE TABLE IF NOT EXISTS gold_world_bank_indicators (
    id inTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT NOT NULL,
    country_name TEXT NOT NULL,
    year INT NOT NULL,
    gdp_current_usd REAL,
    gdp_per_capita_current_usd REAL,
    inflation_percent REAL,
    unemployment_percent REAL,
    population_total REAL
);


DROP TABLE IF EXISTS gold_economic_risk_score;

CREATE TABLE gold_economic_risk_score (
    country_code TEXT NOT NULL,
    country_name TEXT NOT NULL,
    year INTEGER NOT NULL,
    inflation_percent REAL,
    unemployment_percent REAL,
    gdp_growth_percent REAL,
    inflation_score REAL,
    unemployment_score REAL,
    gdp_growth_score REAL,
    final_risk_score REAL,
    risk_level TEXT
);