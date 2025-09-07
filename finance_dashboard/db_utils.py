import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "finance.db"

def create_table(ticker):
    """Cria a tabela no SQLite se não existir"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{ticker}" (
            Data TEXT PRIMARY KEY,
            Faturamento REAL,
            Lucro_Bruto REAL,
            Lucro_Liquido REAL,
            Margem_Lucro REAL,
            Faturamento_Acumulado REAL,
            Last_Update TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_data(ticker, df):
    """Salva ou atualiza os dados no SQLite, garantindo Last_Update"""
    df = df.copy()
    if "Last_Update" not in df.columns:
        df["Last_Update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        df["Last_Update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_FILE)
    df.to_sql(ticker, conn, if_exists='replace', index=False)
    conn.close()

def load_data(ticker):
    """Carrega dados do SQLite; retorna DataFrame vazio se tabela não existir"""
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql(f'SELECT * FROM "{ticker}"', conn)
        conn.close()
        return df
    except:
        conn.close()
        return pd.DataFrame()
