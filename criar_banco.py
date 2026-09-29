import sqlite3

conexao = sqlite3.connect("dados.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS indicadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo INTEGER,
        data TEXT,
        valor REAL,
        UNIQUE(codigo, data)
    )
""")

conexao.commit()
conexao.close()