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
    com nomes de colunas em português e transformando o action_type em colunas distintas.
    Também adiciona novas métricas: cadastro_meta (onsite_conversion.lead_grouped),
    conversas_iniciadas (onsite_conversion.messaging_conversation_started_7d),
    e custo_por_conversa_iniciada.
    """

    # 1) Se o JSON for um dicionário com a chave "data", extrai a lista de anúncios.
    #    Caso contrário, assume que raw_data já seja uma lista de anúncios.
    if isinstance(raw_data, dict) and "data" in raw_data:
        data = raw_data["data"]
    else:
        data = raw_data

    processed_data = []

    # 2) Percorre cada anúncio
    for ad in data:
        # Extrai campos principais
        id_conjunto = str(ad.get("adset_id", ""))
        nome_conjunto = ad.get("adset_name", "Desconhecido")
        data_inicio = ad.get("date_start")
        data_fim = ad.get("date_stop")
        impressoes = int(ad.get("impressions", 0))
        alcance = int(ad.get("reach", 0))
        investimento = float(ad.get("spend", 0.0))

        # Inicializa as variáveis de ação e as métricas
        cliques = 0
        engajamentos = 0
        leads = 0
        conversas_mensagens = 0
        conversao_personalizada = 0

        # Novas variáveis
        cadastro_meta = 0
        conversas_iniciadas = 0  # referente a "onsite_conversion.messaging_conversation_started_7d"

        # 3) Percorre "actions" para somar os valores e criar novas colunas por action_type
        if "actions" in ad and isinstance(ad["actions"], list):
            for action in ad["actions"]:
                action_type = action.get("action_type")
                value = int(action.get("value", 0))

                if action_type == "link_click":
                    cliques += value
                elif action_type == "post_engagement":
                    engajamentos += value
                elif action_type == "lead":
                    leads += value
                elif action_type == "messaging_conversation_started":
                    conversas_mensagens += value
                elif action_type == "custom_conversion":
                    conversao_personalizada += value
                elif action_type == "onsite_conversion.lead_grouped":
                    cadastro_meta += value
                elif action_type == "onsite_conversion.messaging_conversation_started_7d":
                    conversas_iniciadas += value

        # 4) Calcula métricas derivadas
        CTR = round((cliques / impressoes) * 100, 2) if impressoes else 0
        CPL = round(investimento / leads, 2) if leads else 0
        ROI = round((leads * 100) / investimento, 2) if investimento else 0
        CPC = round(investimento / cliques, 2) if cliques else 0
        CR = round((leads / cliques) * 100, 2) if cliques else 0
        custo_por_mensagens = round(investimento / conversas_mensagens, 2) if conversas_mensagens else 0
        custo_por_conversao_personalizada = round(investimento / conversao_personalizada, 2) if conversao_personalizada else 0
        
        # Nova métrica: custo por conversa iniciada
        custo_por_conversa_iniciada = round(investimento / conversas_iniciadas, 2) if conversas_iniciadas else 0

        # 5) Adiciona os dados processados em português
        processed_data.append({
            "id_conjunto": id_conjunto,
            "nome_conjunto": nome_conjunto,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "impressoes": impressoes,
            "alcance": alcance,
            "investimento": investimento,

            # Colunas consolidadas de cada tipo de ação
            "cliques": cliques,
            "engajamentos": engajamentos,
            "leads": leads,
            "conversas_mensagens": conversas_mensagens,
            "conversao_personalizada": conversao_personalizada,
            "cadastro_meta": cadastro_meta,
            "conversas_iniciadas": conversas_iniciadas,

            # Métricas derivadas
            "CTR": CTR,
            "CPL": CPL,
            "ROI": ROI,
            "CPC": CPC,
            "CR": CR,
            "custo_por_mensagens": custo_por_mensagens,
            "custo_por_conversa_iniciada": custo_por_conversa_iniciada,
            "custo_por_conversao_personalizada": custo_por_conversao_personalizada
        })

    return processed_data

def create_dataframe(processed_data):
    """Cria um DataFrame estruturado a partir dos dados processados."""
    df = pd.DataFrame(processed_data)
    return df

# Se rodar diretamente este arquivo, gera o excel também (opcional).
if __name__ == "__main__":
    input_file = "729097561227405_insights2224.json"
    
    # Carrega dados em JSON
    raw_data = load_json(input_file)
    
    # Processa e consolida as métricas
    processed_data = process_json_data(raw_data)
    
    # Cria o DataFrame final
    df = create_dataframe(processed_data)

    # Salva em Excel sem índices
    output_file = "processed_data_caruaru.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Planilha gerada e salva em: {output_file}")
