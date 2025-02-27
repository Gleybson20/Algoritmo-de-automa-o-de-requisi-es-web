import psycopg2

# Configuração para conectar ao PostgreSQL sem um banco específico
conn = psycopg2.connect(
    dbname="Database_Ser",  # Conectar ao banco padrão do PostgreSQL
    user="postgres",
    password="1993",
    host="localhost",
    port="5432"
)
conn.autocommit = True  # Permite criar o banco sem transação ativa

cursor = conn.cursor()

# Nome do banco de dados a ser criado
DATABASE_NAME = "Database_Ser_Educacional"

# Criando o banco de dados
try:
    cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
    print(f"✅ Banco de dados '{DATABASE_NAME}' criado com sucesso!")
except psycopg2.errors.DuplicateDatabase:
    print(f"⚠️ O banco de dados '{DATABASE_NAME}' já existe.")

# Fechar conexão
cursor.close()
conn.close()
