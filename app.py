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

# Cartões de resumo
dolar_hoje = dolar["valor"].iloc[-1]
dolar_ontem = dolar["valor"].iloc[-2]
selic_hoje = selic["valor"].iloc[-1]
ipca_ultimo = ipca["valor"].iloc[-1]
ipca_mes = ipca["data"].iloc[-1].strftime("%m/%Y")

col1, col2, col3 = st.columns(3)
col1.metric("Dólar (R$)", f"{dolar_hoje:.4f}", f"{dolar_hoje - dolar_ontem:+.4f}")
col2.metric("Selic (% ao ano)", f"{selic_hoje:.2f}%")
col3.metric(f"IPCA {ipca_mes}", f"{ipca_ultimo:.2f}%")


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
ipca_grafico = ipca.copy()
ipca_grafico["mes"] = ipca_grafico["data"].dt.strftime("%Y-%m")
grafico_ipca = (
    alt.Chart(ipca_grafico)
    .mark_bar()
    .encode(
        x=alt.X("mes:O", title="Mês"),
        y=alt.Y("valor:Q", title="Variação (%)"),
    )
)
st.altair_chart(grafico_ipca)

st.subheader("Todos os dados")
tabela = df.sort_values("data", ascending=False).copy()
tabela["data"] = tabela["data"].dt.strftime("%Y-%m-%d")
st.dataframe(tabela)