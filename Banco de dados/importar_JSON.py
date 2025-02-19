import os
import json
import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "ads_database_ser",
    "user": "postgres",
    "password": "1993",
    "host": "localhost",
    "port": "5432"
}

# Definir a pasta onde os arquivos JSON estão localizados
pasta_json = r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\kjl"

def importar_json():
    """Importa todos os arquivos JSON da pasta para o PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Lista para armazenar os dados que serão inseridos
        dados_para_inserir = []

        # Percorrendo os arquivos JSON na pasta especificada
        for arquivo in os.listdir(pasta_json):
            if arquivo.endswith(".json"):
                caminho_completo = os.path.join(pasta_json, arquivo)
                print(f"📂 Processando JSON: {arquivo}")

                # Ler o arquivo JSON
                with open(caminho_completo, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Inserir os dados no PostgreSQL
                for entry in data:
                    id_conta = entry.get("account_id")
                    id_conjunto = entry.get("adset_id")
                    nome_conjunto = entry.get("adset_name")
                    id_anuncio = entry.get("ad_id")
                    nome_anuncio = entry.get("ad_name")
                    data = entry.get("date_start")
                    investimento = float(entry.get("spend", 0))  # Investimento
                    
                    # Inicializar métricas extraídas da lista de "actions"
                    cliques = 0
                    leads = 0
                    cadastro_meta = 0
                    conversas_iniciadas = 0

                    # Percorrer a lista de ações dentro do JSON para extrair métricas específicas
                    for action in entry.get("actions", []):
                        if action["action_type"] == "link_click":
                            cliques = int(action.get("value", 0))
                        elif action["action_type"] == "lead":
                            leads = int(action.get("value", 0))
                        elif action["action_type"] == "onsite_conversion.lead_grouped":
                            cadastro_meta = int(action.get("value", 0))
                        elif action["action_type"] == "onsite_conversion.messaging_conversation_started_7d":
                            conversas_iniciadas = int(action.get("value", 0))

                    # Adicionar os dados para inserção em lote
                    dados_para_inserir.append((
                        id_conta, id_conjunto, nome_conjunto, id_anuncio, nome_anuncio,
                        data, investimento, cliques, leads,
                        cadastro_meta, conversas_iniciadas
                    ))

                print(f"✅ JSON '{arquivo}' processado com sucesso!")

        # Inserir todos os dados de uma vez
        cursor.executemany("""
            INSERT INTO anuncios_json (
                id_conta, id_conjunto, nome_conjunto, id_anuncio, nome_anuncio,
                data, investimento, cliques, leads, cadastro_meta, conversas_iniciadas
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, dados_para_inserir)

        conn.commit()

        # Fechar a conexão
        cursor.close()
        conn.close()
        print("🎉 Importação de JSON concluída!")

    except Exception as e:
        print(f"❌ Erro ao importar JSON: {e}")

# Rodar o script
if __name__ == "__main__":
    importar_json()
