# Dashboard de Indicadores Econômicos

Dashboard com dados reais do Banco Central do Brasil (dólar, Selic e IPCA) que **se atualiza sozinho todo dia útil**, sem ninguém precisar rodar nada.

**Dashboard ao vivo: https://indicadores-economicos-lucas.streamlit.app**

> Se a página mostrar um botão para "acordar" o app, é só clicar. No plano gratuito do Streamlit ele dorme quando fica um tempo sem acesso e volta em alguns segundos.

<!-- Quando tiver um print do dashboard, salve em img/dashboard.png e descomente a linha abaixo -->
<!-- ![Dashboard](img/dashboard.png) -->

---

## Sobre o projeto

Os meus projetos anteriores usavam dados estáticos (CSV baixado uma vez). Aqui eu quis o oposto: uma **fonte de dados real, que muda todo dia**, com a coleta, o armazenamento, a atualização e a visualização funcionando de ponta a ponta.

O projeto responde, de forma simples, três perguntas sobre o último ano da economia brasileira:

- Como o dólar se comportou?
- O que o Banco Central fez com a taxa de juros (Selic)?
- A inflação (IPCA) está acelerando ou desacelerando?

## O que os dados mostram

*Leitura feita em 09/10/2026, com um ano de dados (de 08/10/2025 até hoje).*

**Dólar: caiu no ano, mas não em linha reta.**
Começou o período em R$ 5,34, chegou ao pico de R$ 5,57 em 29/12/2025 e despencou até a mínima de R$ 4,90 em 11/05/2026 (queda de uns 12% do pico ao vale). Depois recuperou um pouco e fecha a série em R$ 5,01. No saldo, é uns 6% abaixo do início. Dizer só que "o dólar caiu" esconderia esse sobe e desce.

**Selic: cortes em degraus.**
A meta começou o período perto de 15% e foi reduzida aos poucos. O último corte foi de 14,00% para 13,75%, em 17/09/2026. O gráfico tem formato de escada porque a Selic **não é medida todo dia**: ela é uma meta definida pelo Copom, que vale até a próxima reunião.

**IPCA: inflação desacelerando.**
O IPCA mensal teve o pico em março de 2026 (0,88%) e foi esfriando até agosto, que foi o **único mês negativo** da série: -0,32% (deflação). Preço subindo mais devagar não é o mesmo que preço caindo, e agosto foi o único mês em que o índice realmente recuou.

**Uma hipótese (não uma conclusão).**
Os três indicadores andaram para baixo no mesmo período, o que é coerente com a ideia de que o Banco Central corta os juros quando a inflação desacelera. Mas com só um ano de dados e três séries, isso é uma **hipótese**: não dá para afirmar causa e efeito com esses dados.

## Como funciona

```
API do Banco Central (SGS)
        |
        v
coletar_dados.py  --->  dados.db (SQLite)  --->  app.py (Streamlit)  --->  link público
        ^                      |
        |                      v
GitHub Actions (seg-sex, 20h de Brasília): roda a coleta e
faz commit do banco atualizado de volta no repositório
```

1. **Coleta:** o `coletar_dados.py` busca os últimos 365 dias de cada indicador na API pública do Bacen (sem chave de acesso).
2. **Armazenamento:** os dados vão para uma tabela SQLite. A regra `UNIQUE(codigo, data)` junto com `INSERT OR IGNORE` garante que rodar o script várias vezes **nunca duplica** linhas.
3. **Atualização automática:** um workflow do GitHub Actions roda de segunda a sexta, instala as dependências, executa a coleta e, se o banco mudou, commita o `dados.db` sozinho (os commits do robô aparecem como `github-actions[bot]`).
4. **Visualização:** o Streamlit lê o banco e monta cartões de resumo, gráficos e a tabela. Como o app está ligado ao repositório, ele acompanha os commits do robô.

## Tecnologias

- **Python:** `requests`, `sqlite3`, `pandas`, `datetime`
- **SQLite:** banco em um único arquivo
- **Streamlit** + **Altair:** dashboard e gráficos
- **GitHub Actions:** agendamento e atualização automática
- **Git/GitHub:** versionamento, com commits separados por etapa do projeto

## Indicadores usados (API SGS do Bacen)

| Código | Indicador | Frequência |
|---|---|---|
| 1 | Dólar comercial (venda) | diária (dias úteis) |
| 432 | Selic (meta) | diária |
| 433 | IPCA (variação mensal) | mensal |

## Estrutura do repositório

```
├── .github/workflows/atualizar.yml   # robô de atualização automática
├── app.py                            # dashboard (Streamlit)
├── coletar_dados.py                  # coleta na API e grava no SQLite
├── criar_banco.py                    # cria a tabela do banco
├── dados.db                          # banco SQLite (atualizado pelo robô)
├── requirements.txt                  # dependências
└── teste_api.py                      #