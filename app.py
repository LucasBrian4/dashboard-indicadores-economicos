import sqlite3
import altair as alt
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
selic = df[df["codigo"] == 432]
ipca = df[df["codigo"] == 433]


def grafico_linha(dados):
    return (
        alt.Chart(dados)
        .mark_line()
        .encode(
            x="data:T",
            y=alt.Y("valor:Q", scale=alt.Scale(zero=False)),
        )
    )


st.subheader("Dólar comercial (venda)")
st.altair_chart(grafico_linha(dolar))

st.subheader("Selic (meta, % ao ano)")
st.altair_chart(grafico_linha(selic))

st.subheader("IPCA (variação mensal, %)")
st.bar_chart(ipca, x="data", y="valor")

st.subheader("Todos os dados")
st.dataframe(df.sort_values("data", ascending=False))