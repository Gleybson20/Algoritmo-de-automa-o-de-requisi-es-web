import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "Database_Ser_Educacional",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

# Função para criar as tabelas
def criar_tabelas():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1. Criar a tabela de unidades
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS unidades (
            id_conta BIGINT PRIMARY KEY,   -- ID da conta
            nome_unidade TEXT NOT NULL     -- Nome da unidade (ex: 'Cabo', 'Cacoal', etc.)
        );
        """)

        # 2. Criar a tabela de anuncios_json
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS anuncios_json (
            id SERIAL PRIMARY KEY,           -- Identificador único para cada entrada
            id_conta BIGINT NOT NULL,        -- ID da conta
            id_conjunto BIGINT,              -- ID do conjunto de anúncios
            nome_conjunto TEXT,              -- Nome do conjunto de anúncios
            id_anuncio BIGINT NOT NULL,      -- ID do anúncio
            nome_anuncio TEXT,               -- Nome do anúncio
            data DATE,                -- Data de início do anúncio
            investimento NUMERIC(10,2),      -- Investimento total
            cliques INT,                     -- Total de cliques
            leads INT,                       -- Total de leads
            cadastro_meta INT,               -- Total de cadastros meta
            conversas_iniciadas INT         -- Total de conversas iniciadas
        );
        """)

        # Confirmar as alterações no banco de dados
        conn.commit()
        print("✅ Tabela criadas com sucesso!")

        # Fechar a conexão
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erro ao criar as tabela: {e}")

if __name__ == "__main__":
    criar_tabelas()
