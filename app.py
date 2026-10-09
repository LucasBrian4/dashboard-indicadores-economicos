import sqlite3
import pandas as pd
import streamlit as st

st.title("Indicadores Econômicos")

conexao = sqlite3.connect("dados.db")
df = pd.read_sql_query(
    "SELECT codigo, data, valor FROM indicadores ORDER BY data",
    conexao,
)
conexao.close()

df["data"] = pd.to_datetime(df["data"])

dolar = df[df["codigo"] == 1]

st.subheader("Dólar comercial (venda)")
st.line_chart(dolar, x="data", y="valor")

st.subheader("Todos os dados")
st.dataframe(df.sort_values("data", ascending=False))