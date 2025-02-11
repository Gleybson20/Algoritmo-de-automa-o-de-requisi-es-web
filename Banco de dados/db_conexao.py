import psycopg2

# Configurações do banco de dados
DB_CONFIG = {
    "dbname": "ads_database_ser",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

def conectar_banco():
    """Estabelece conexão com o PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Conexão bem-sucedida com o PostgreSQL!")
        return conn, cursor
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None, None

if __name__ == "__main__":
    conn, cursor = conectar_banco()

    if conn:
        # Criando uma tabela para armazenar JSON
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dados_json (
                id SERIAL PRIMARY KEY,
                nome_arquivo TEXT NOT NULL,
                conteudo JSONB NOT NULL,
                data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("📌 Tabela 'dados_json' criada para armazenar JSON!")

        cursor.close()
        conn.close()
        print("🔒 Conexão fechada.")
