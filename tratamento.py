import os
import json
import csv

# Definir a pasta onde os arquivos JSON estão localizados
pasta_json = r"D:\Users\gras2\Algoritmo-de-automa-o-de-requisi-es-web\2025 atualizações do ano"
output_csv = r"D:\Users\gras2\Algoritmo-de-automa-o-de-requisi-es-web\planilha.csv"  # Caminho do arquivo CSV de saída

def importar_json_para_csv():
    """Importa todos os arquivos JSON da pasta e grava no CSV com uma coluna id"""
    try:
        # Lista para armazenar os dados que serão inseridos no CSV
        dados_para_inserir = []
        id_counter = 1  # Inicializar o contador de ID

        # Percorrendo os arquivos JSON na pasta especificada
        for arquivo in os.listdir(pasta_json):
            if arquivo.endswith(".json"):
                caminho_completo = os.path.join(pasta_json, arquivo)
                print(f"📂 Processando JSON: {arquivo}")

                # Ler o arquivo JSON
                with open(caminho_completo, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Extrair os dados do JSON
                for entry in data:
                    id_conta = entry.get("account_id")
                    id_conjunto = entry.get("adset_id")
                    nome_conjunto = entry.get("adset_name")
                    id_anuncio = entry.get("ad_id")
                    nome_anuncio = entry.get("ad_name")
                    data_inicio = entry.get("date_start")
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

                    # Adicionar os dados para a lista que será gravada no CSV
                    dados_para_inserir.append([
                        id_counter,  # ID único
                        id_conta, id_conjunto, nome_conjunto, id_anuncio, nome_anuncio,
                        data_inicio, investimento, cliques, leads,
                        cadastro_meta, conversas_iniciadas
                    ])

                    # Incrementar o contador para o próximo ID
                    id_counter += 1

                print(f"✅ JSON '{arquivo}' processado com sucesso!")

        # Escrever os dados no arquivo CSV
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escrever o cabeçalho do CSV, incluindo a coluna ID
            writer.writerow([
                "id", "id_conta", "id_conjunto", "nome_conjunto", "id_anuncio", "nome_anuncio",
                "data", "investimento", "cliques", "leads",
                "cadastro_meta", "conversas_iniciadas"
            ])

            # Escrever os dados
            writer.writerows(dados_para_inserir)

        print(f"🎉 Importação de JSON para CSV concluída com sucesso! O arquivo está salvo em {output_csv}")

    except Exception as e:
        print(f"❌ Erro ao importar JSON para CSV: {e}")

# Rodar o script
if __name__ == "__main__":
    importar_json_para_csv()
