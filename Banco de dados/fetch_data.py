import psycopg2
import pandas as pd

DB_CONFIG = {
    "dbname": "ads_database_ser",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

def obter_relatorio():
    """Consulta a view de insights e exibe os dados"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = "SELECT * FROM relatorio_geral ORDER BY data_inicio;"
        df = pd.read_sql(query, conn)
        conn.close()
        
        return df

    except Exception as e:
        print(f"Erro na consulta: {e}")
        return None

# Executar a consulta e exibir os dados
df_insights = obter_relatorio()
print(df_insights)
