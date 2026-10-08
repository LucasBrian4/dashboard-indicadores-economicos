import sqlite3
import requests

conexao = sqlite3.connect("dados.db")
cursor = conexao.cursor()

codigos = [1, 432, 433]  # dólar, Selic, IPCA

for codigo in codigos:
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/10?formato=json"
    dados = requests.get(url).json()

    for item in dados:
        cursor.execute(
            "INSERT OR IGNORE INTO indicadores (codigo, data, valor) VALUES (?, ?, ?)",
            (codigo, item["data"], float(item["valor"])),
        )

conexao.commit()
conexao.close()
print("Dados salvos")