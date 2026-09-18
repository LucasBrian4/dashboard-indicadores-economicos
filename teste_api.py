import requests

codigo = 433  # 1, 432 ou 433

url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/10?formato=json"

resposta = requests.get(url)
dados = resposta.json()

for item in dados:
    print(item["data"], item["valor"])