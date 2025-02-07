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
    """
    Processa os dados extraindo colunas diretas e adiciona métricas calculadas,
    consolidando todas as actions em apenas UMA linha por anúncio/conjunto (data).
    Agora a coluna 'gasto' foi renomeada para 'investimento'.
    Inclui novos tipos de ação: onsite_conversion.lead_grouped e
    onsite_conversion.messaging_conversation_started_7d.
    """
    processed_data = []
    
    # Percorre o array principal
    for block in data:
        # Verifica se há dados ("data") no bloco
        if "data" not in block:
            continue
        
        # Percorre cada anúncio (ad) dentro de block["data"]
        for ad in block["data"]:
            adset_id = str(ad.get("adset_id"))
            adset_name = ad.get("adset_name", "Desconhecido")
            date_start = ad.get("date_start")
            date_stop = ad.get("date_stop")
            impressions = int(ad.get("impressions", 0))
            reach = int(ad.get("reach", 0))
            
            # 'investimento' em vez de 'gasto'
            investimento = float(ad.get("spend", 0.0))
            
            # Inicializa variáveis de ação
            clicks = 0
            engagements = 0
            leads = 0
            messaging_conversation_started = 0
            custom_conversion = 0
            
            # Novas métricas (agrupadas)
            onsite_conversion_lead_grouped = 0
            onsite_conversion_messaging_conversation_started_7d = 0
            
            # Se existirem ações, somamos os valores
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
                    
                    # Novos tipos de ação
                    elif action_type == "onsite_conversion.lead_grouped":
                        onsite_conversion_lead_grouped += value
                    elif action_type == "onsite_conversion.messaging_conversation_started_7d":
                        onsite_conversion_messaging_conversation_started_7d += value
            
            # Cálculo de métricas derivadas
            CTR = round((clicks / impressions) * 100, 2) if impressions else 0
            CPL = round(investimento / leads, 2) if leads else 0
            ROI = round((leads * 100) / investimento, 2) if investimento else 0
            CPC = round(investimento / clicks, 2) if clicks else 0
            CR = round((leads / clicks) * 100, 2) if clicks else 0
            
            # Se você ainda quiser manter o custo por mensagens do "messaging_conversation_started" original:
            custo_por_mensagens = round(investimento / messaging_conversation_started, 2) if messaging_conversation_started else 0
            
            # Para os novos tipos de ação:
            custo_por_cadastro = round(investimento / onsite_conversion_lead_grouped, 2) if onsite_conversion_lead_grouped else 0
            custo_por_conversa_iniciada = round(
                investimento / onsite_conversion_messaging_conversation_started_7d, 2
            ) if onsite_conversion_messaging_conversation_started_7d else 0
            
            # Para a conversão personalizada
            custo_por_conversao_personalizada = round(investimento / custom_conversion, 2) if custom_conversion else 0
            
            # Cria UM registro consolidado para este anúncio
            processed_data.append({
                "id_conjunto": adset_id,
                "nome_conjunto": adset_name,
                "data_inicio": date_start,
                "data_fim": date_stop,
                "impressoes": impressions,
                "alcance": reach,
                "investimento": investimento,
                
                # Métricas de ação antigas
                "cliques": clicks,
                "engajamentos": engagements,
                "leads": leads,
                "conversas_mensagens": messaging_conversation_started,
                "conversao_personalizada": custom_conversion,
                
                # Novas colunas (dos novos tipos de ação)
                "cadastro_meta": onsite_conversion_lead_grouped,
                "conversas_iniciadas": onsite_conversion_messaging_conversation_started_7d,
                
                # Métricas derivadas
                "CTR": CTR,
                "CPL": CPL,
                "ROI": ROI,
                "CPC": CPC,
                "CR": CR,
                "custo_por_mensagens": custo_por_mensagens,
                "custo_por_cadastro": custo_por_cadastro,
                "custo_por_conversa_iniciada": custo_por_conversa_iniciada,
                "custo_por_conversao_personalizada": custo_por_conversao_personalizada
            })
    
    return processed_data

def create_dataframe(processed_data):
    """Cria um DataFrame estruturado a partir dos dados processados."""
    df = pd.DataFrame(processed_data)
    return df

if __name__ == "__main__":
    input_file = "insights2224.json"
    
    # 1. Carrega o JSON
    raw_data = load_json(input_file)
    
    # 2. Processa e consolida as métricas
    processed_data = process_json_data(raw_data)
    
    # 3. Cria o DataFrame final
    df = create_dataframe(processed_data)
    
    # Exemplo de saída no console
    print(df.head())
