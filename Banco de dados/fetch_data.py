import psycopg2

DB_CONFIG = {
    "dbname": "ads_database_ser",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Buscar todos os usuários
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

print("\n📌 Lista de Usuários no Banco de Dados:")
for usuario in usuarios:
    print(usuario)

cursor.close()
conn.close()
