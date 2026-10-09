import sqlite3
import pandas as pd
import streamlit as st

st.title("Indicadores Econômicos")

conexao = sqlite3.connect("dados.db")
df = pd.read_sql_query(
    "SELECT codigo, data, valor FROM indicadores ORDER BY data DESC",
    conexao,
)
conexao.close()

st.dataframe(df)