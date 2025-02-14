import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "ads_database_ser",
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
            data_inicio DATE,                -- Data de início do anúncio
            data_fim DATE,                   -- Data de fim do anúncio
            investimento NUMERIC(10,2),      -- Investimento total
            cliques INT,                     -- Total de cliques
            leads INT,                       -- Total de leads
            cadastro_meta INT,               -- Total de cadastros meta
            conversas_iniciadas INT         -- Total de conversas iniciadas
        );
        """)

        # 3. Criar a tabela de metricas_mensais
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metricas_mensais (
            id SERIAL PRIMARY KEY,
            mes DATE NOT NULL,               -- Mês da análise (exemplo: '2024-01-01' para janeiro de 2024)
            unidade TEXT NOT NULL,           -- Unidade associada ao mês
            investimento_total NUMERIC(10,2) NOT NULL,  -- Total investido no mês
            cliques_total INT NOT NULL DEFAULT 0,       -- Total de cliques no mês
            leads_total INT NOT NULL DEFAULT 0,         -- Total de leads no mês
            conversas_total INT NOT NULL DEFAULT 0,     -- Total de conversas iniciadas no mês
            cadastros_total INT NOT NULL DEFAULT 0,     -- Total de cadastros meta no mês
            custo_por_conversa NUMERIC(10,2),           -- Custo médio por conversa iniciada
            custo_por_lead NUMERIC(10,2),               -- Custo médio por lead
            custo_por_cadastro NUMERIC(10,2),            -- Custo médio por cadastro meta
            UNIQUE (unidade, mes)  -- Evita duplicação para o mesmo mês e unidade
        );
        """)

        # 4. Criar a tabela de analises_temporais
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analises_temporais (
            id SERIAL PRIMARY KEY,
            mes_atual DATE NOT NULL,    -- Mês de referência
            mes_anterior DATE,          -- Mês anterior para comparações
            unidade TEXT NOT NULL,      -- Unidade associada ao mês
            investimento_total NUMERIC(10,2) NOT NULL, -- Investimento total do mês
            investimento_mes_anterior NUMERIC(10,2),  -- Investimento no mês anterior
            variacao_investimento NUMERIC(10,2),       -- Diferença percentual do investimento entre meses
            cliques_total INT NOT NULL DEFAULT 0,      -- Total de cliques no mês
            cliques_mes_anterior INT,                   -- Total de cliques no mês anterior
            variacao_cliques NUMERIC(10,2),            -- Diferença percentual dos cliques entre meses
            roi NUMERIC(10,2),                          -- Retorno sobre investimento (ROI)
            taxa_conversao_lead NUMERIC(10,2),         -- Taxa de conversão de leads (Leads / Conversas)
            taxa_conversao_cadastro NUMERIC(10,2),     -- Taxa de conversão de cadastros (Cadastros / Leads)
            UNIQUE (unidade, mes_atual)  -- Evita duplicação para o mesmo mês e unidade
        );
        """)

        # Confirmar as alterações no banco de dados
        conn.commit()
        print("✅ Tabelas criadas com sucesso!")

        # Fechar a conexão
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erro ao criar as tabelas: {e}")

if __name__ == "__main__":
    criar_tabelas()
