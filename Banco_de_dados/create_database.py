import psycopg2
from psycopg2 import sql

# Configuração para conectar ao PostgreSQL (sem especificar banco de dados)
try:
    # Conectar ao PostgreSQL, usando banco de dados padrão 'postgres'
    conn = psycopg2.connect(
        dbname="postgres",  # Banco padrão para conexão
        user="postgres",    # Seu usuário
        password="1993",    # Sua senha
        host="localhost",   # Host (pode ser 'localhost' se estiver local)
        port="5432"         # Porta padrão do PostgreSQL
    )
    conn.autocommit = True  # Permite criar o banco sem transação ativa

    # Criação do cursor
    cursor = conn.cursor()

    # Nome do banco de dados a ser criado
    DATABASE_NAME = "doze-dezesseis"

    # Teste de conexão simples para verificar se a conexão foi bem-sucedida
    cursor.execute("SELECT 1;")
    print("✅ Conexão bem-sucedida!")

    # Criando o banco de dados
    try:
        # Usando a função sql.Identifier para evitar problemas com injeções de SQL
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_NAME)))
        print(f"✅ Banco de dados '{DATABASE_NAME}' criado com sucesso!")
    except psycopg2.errors.DuplicateDatabase:
        print(f"⚠️ O banco de dados '{DATABASE_NAME}' já existe.")
    
    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
