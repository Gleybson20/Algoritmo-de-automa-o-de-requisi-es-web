import pandas as pd
import psycopg2

DB_CONFIG = {
    "dbname": "ads_database_ser",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

def importar_excel(arquivo_excel):
    """Importa dados de uma planilha Excel para o PostgreSQL."""
    try:
        # Carregar a planilha para um DataFrame
        df = pd.read_excel(arquivo_excel, engine="openpyxl")

        # Conectar ao PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Inserir cada linha da planilha no banco
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO anuncios_excel (
                    id_conta, id_conjunto, nome_conjunto, data_inicio, impressoes, alcance, 
                    investimento, cliques, leads, cadastro_meta, conversas_iniciadas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row["id_conta"], row["id_conjunto"], row["nome_conjunto"], row["data_inicio"],
                row["impressoes"], row["alcance"], row["investimento"], row["cliques"], row["leads"],
                row["cadastro_meta"], row["conversas_iniciadas"]
            ))

        conn.commit()
        print("✅ Planilha importada com sucesso!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erro ao importar Excel: {e}")

if __name__ == "__main__":
    importar_excel(r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\Planilhas\novo_processed_data_carpipna.xlsx")
