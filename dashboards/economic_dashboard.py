import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(ROOT_DIR))

from config import DATABASE_PATH


import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st




st.set_page_config(
    page_title="Economic Risk Monitor",
    layout="wide"
)

st.title("📊 Economic Risk Monitor")
st.write("Dashboard para análise de risco econômico com dados da World Bank API.")

connection = sqlite3.connect(DATABASE_PATH)

df = pd.read_sql_query(
    "SELECT * FROM gold_economic_risk_score",
    connection
)

countries = sorted(df["country_name"].unique())

selected_country = st.selectbox(
    "Selecione um país",
    countries
)

filtered_df = df[df["country_name"] == selected_country]

st.subheader(f"Análise econômica: {selected_country}")

latest_year = filtered_df["year"].max()
latest_data = filtered_df[filtered_df["year"] == latest_year].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Score de Risco",
    round(latest_data["final_risk_score"], 2)
)

col2.metric(
    "Nível de Risco",
    latest_data["risk_level"]
)

col3.metric(
    "Ano mais recente",
    int(latest_year)
)

fig_score = px.line(
    filtered_df,
    x="year",
    y="final_risk_score",
    markers=True,
    title=f"Evolução do Score de Risco - {selected_country}"
)

st.plotly_chart(fig_score, use_container_width=True)

fig_indicators = px.line(
    filtered_df,
    x="year",
    y=[
        "inflation_percent",
        "unemployment_percent",
        "gdp_growth_percent"
    ],
    markers=True,
    title=f"Indicadores Econômicos - {selected_country}"
)

st.plotly_chart(fig_indicators, use_container_width=True)

st.subheader("Tabela Analítica")
st.dataframe(filtered_df, use_container_width=True)