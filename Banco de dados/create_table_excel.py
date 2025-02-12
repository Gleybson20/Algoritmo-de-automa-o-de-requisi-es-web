import psycopg2

DB_CONFIG = {
    "dbname": "ads_database_ser",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

def criar_tabela():
    """Cria uma tabela no PostgreSQL para armazenar os dados do Excel."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anuncios_excel (
                id SERIAL PRIMARY KEY,
                id_conta TEXT,
                id_conjunto TEXT,
                nome_conjunto TEXT,
                data_inicio DATE,
                impressoes INT,
                alcance INT,
                investimento FLOAT,
                cliques INT,
                leads INT,
                cadastro_meta INT,
                conversas_iniciadas INT
            )
        """)

        conn.commit()
        print("✅ Tabela 'anuncios_excel' criada/atualizada com sucesso!")

        cursor.close()
        conn.close()
    
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")

if __name__ == "__main__":
    criar_tabela()
