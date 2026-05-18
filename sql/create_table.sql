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