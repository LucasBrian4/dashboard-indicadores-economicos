import sqlite3
import requests
from datetime import datetime, timedelta

conexao = sqlite3.connect("dados.db")
cursor = conexao.cursor()

codigos = [1, 432, 433]  # dólar, Selic, IPCA

hoje = datetime.today()
data_final = hoje.strftime("%d/%m/%Y")
data_inicial = (hoje - timedelta(days=365)).strftime("%d/%m/%Y")

for codigo in codigos:
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
        f"?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    )
    dados = requests.get(url).json()

    for item in dados:
        data_iso = datetime.strptime(item["data"], "%d/%m/%Y").strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT OR IGNORE INTO indicadores (codigo, data, valor) VALUES (?, ?, ?)",
            (codigo, data_iso, float(item["valor"])),
        )

conexao.commit()
conexao.close()
print("Dados salvos")