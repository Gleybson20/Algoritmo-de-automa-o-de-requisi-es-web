import json
import pandas as pd
from datetime import datetime

def load_json(file_path):
    """Carrega o arquivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Erro ao carregar JSON: {e}")
            return []
    return data

def process_json_data(data):
    """Processa os dados extraindo colunas diretas e adiciona métricas calculadas."""
    processed_data = []
    
    for block in data:
        if "data" in block:
            for ad in block["data"]:
                adset_id = str(ad.get("adset_id"))
                adset_name = ad.get("adset_name", "Desconhecido")
                date_start = ad.get("date_start")
                date_stop = ad.get("date_stop")
                impressions = int(ad.get("impressions", 0))
                reach = int(ad.get("reach", 0))
                spend = float(ad.get("spend", 0.0))
                
                # Inicializa métricas calculadas
                clicks = 0
                engagements = 0
                leads = 0
                messaging_conversation_started = 0
                custom_conversion = 0
                
                # Verifica se existem ações e cria uma linha para cada action_type
                if "actions" in ad:
                    for action in ad["actions"]:
                        action_type = action.get("action_type")
                        value = int(action.get("value", 0))
                        
                        if action_type == "link_click":
                            clicks += value
                        elif action_type == "post_engagement":
                            engagements += value
                        elif action_type == "lead":
                            leads += value
                        elif action_type == "messaging_conversation_started":
                            messaging_conversation_started += value
                        elif action_type == "custom_conversion":
                            custom_conversion += value
                        
                        # Calcula métricas derivadas
                        CTR = round((clicks / impressions) * 100 if impressions > 0 else 0, 2)
                        CPL = round(spend / leads if leads > 0 else 0, 2)
                        ROI = round((leads * 100) / spend if spend > 0 else 0, 2)
                        CPC = round(spend / clicks if clicks > 0 else 0, 2)
                        CPA = round(spend / leads if leads > 0 else 0, 2)
                        CR = round((leads / clicks) * 100 if clicks > 0 else 0, 2)
                        cost_per_messaging_conversation = round(spend / messaging_conversation_started if messaging_conversation_started > 0 else 0, 2)
                        cost_per_custom_conversion = round(spend / custom_conversion if custom_conversion > 0 else 0, 2)
                        
                        processed_data.append({
                            "adset_id": adset_id,
                            "adset_name": adset_name,
                            "date_start": date_start,
                            "date_stop": date_stop,
                            "impressions": impressions,
                            "reach": reach,
                            "spend": spend,
                            "action_type": action_type,
                            "value": value,
                            "clicks": clicks,
                            "engagements": engagements,
                            "leads": leads,
                            "messaging_conversation_started": messaging_conversation_started,
                            "custom_conversion": custom_conversion,
                            "CTR": CTR,
                            "CPL": CPL,
                            "ROI": ROI,
                            "CPC": CPC,
                            "CPA": CPA,
                            "CR": CR,
                            "cost_per_messaging_conversation": cost_per_messaging_conversation,
                            "cost_per_custom_conversion": cost_per_custom_conversion
                        })
                else:
                    # Caso não existam ações, cria uma linha sem action_type e sem métricas calculadas
                    processed_data.append({
                        "adset_id": adset_id,
                        "adset_name": adset_name,
                        "date_start": date_start,
                        "date_stop": date_stop,
                        "impressions": impressions,
                        "reach": reach,
                        "spend": spend,
                        "action_type": None,
                        "value": 0,
                        "clicks": clicks,
                        "engagements": engagements,
                        "leads": leads,
                        "messaging_conversation_started": messaging_conversation_started,
                        "custom_conversion": custom_conversion,
                        "CTR": 0,
                        "CPL": 0,
                        "ROI": 0,
                        "CPC": 0,
                        "CPA": 0,
                        "CR": 0,
                        "cost_per_messaging_conversation": 0,
                        "cost_per_custom_conversion": 0
                    })
    
    return processed_data

def create_dataframe(processed_data):
    """Cria um DataFrame estruturado a partir dos dados processados."""
    df = pd.DataFrame(processed_data)
    return df

if __name__ == "__main__":
    input_file = "insights2224.json"
    raw_data = load_json(input_file)
    processed_data = process_json_data(raw_data)
    df = create_dataframe(processed_data)
    print(df.head())
