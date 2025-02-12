import os
import pandas as pd
import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "ads_database_ser",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

# Lista de arquivos a serem importados
arquivos_planilhas = [
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\Planilhas\novo_processed_data_carpipna.xlsx",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\Planilhas\novo_processed_data_curitiba.xlsx",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\Planilhas\novo_processed_data_garanhus.xlsx",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\Planilhas\novo_processed_data_paulista.xlsx"
]

def importar_todas_planilhas():
    """Importa uma lista de planilhas para o PostgreSQL"""
    try:
        # Conectar ao banco
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Percorrer todas as planilhas da lista
        for caminho_completo in arquivos_planilhas:
            if caminho_completo.endswith(".xlsx"):  # Garantia de que é Excel
                nome_arquivo = os.path.basename(caminho_completo)

                # Ler a planilha em um DataFrame
                df = pd.read_excel(caminho_completo, engine="openpyxl")

                # Inserir os dados no PostgreSQL
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

                print(f"✅ Planilha '{nome_arquivo}' importada com sucesso!")

        # Commit e fechamento da conexão
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erro ao importar planilhas: {e}")

if __name__ == "__main__":
    importar_todas_planilhas()
