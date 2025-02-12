import json
import pandas as pd

def load_json(file_path):
    """Carrega o arquivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Erro ao carregar JSON: {e}")
            return []
    return data

def process_json_data(raw_data):
    """
    Processa os dados extraindo colunas diretas e adiciona métricas calculadas,
    mantendo nomes de colunas em português e transformando action_type em colunas distintas.
    Agora inclui account_id e remove CPL, CPC, CR e CTR.
    """
    if isinstance(raw_data, dict) and "data" in raw_data:
        data = raw_data["data"]
    else:
        data = raw_data

    processed_data = []

    for ad in data:
        id_conta = str(ad.get("account_id", ""))
        id_conjunto = str(ad.get("adset_id", ""))
        nome_conjunto = ad.get("adset_name", "Desconhecido")
        data_inicio = ad.get("date_start")
        impressoes = int(ad.get("impressions", 0))
        alcance = int(ad.get("reach", 0))
        investimento = float(ad.get("spend", 0.0))

        cliques = 0
        leads = 0
        cadastro_meta = 0
        conversas_iniciadas = 0

        if "actions" in ad and isinstance(ad["actions"], list):
            for action in ad["actions"]:
                action_type = action.get("action_type")
                value = int(action.get("value", 0))

                if action_type == "link_click":
                    cliques += value
                elif action_type == "lead":
                    leads += value
                elif action_type == "onsite_conversion.lead_grouped":
                    cadastro_meta += value
                elif action_type == "onsite_conversion.messaging_conversation_started_7d":
                    conversas_iniciadas += value

        processed_data.append({
            "id_conta": id_conta,
            "id_conjunto": id_conjunto,
            "nome_conjunto": nome_conjunto,
            "data_inicio": data_inicio,
            "impressoes": impressoes,
            "alcance": alcance,
            "investimento": investimento,
            "cliques": cliques,
            "leads": leads,
            "cadastro_meta": cadastro_meta,
            "conversas_iniciadas": conversas_iniciadas
        })
    return processed_data

def create_dataframe(processed_data):
    """Cria um DataFrame estruturado a partir dos dados processados."""
    df = pd.DataFrame(processed_data)
    return df

if __name__ == "__main__":
    input_file = "1213925972283556_insights2224.json"
    raw_data = load_json(input_file)
    processed_data = process_json_data(raw_data)
    df = create_dataframe(processed_data)
    output_file = "novo_processed_data_garanhus.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Planilha gerada e salva em: {output_file}")
