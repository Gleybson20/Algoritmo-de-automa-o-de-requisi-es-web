import json
import requests
import time
import os
from datetime import datetime, timedelta
from supabase import create_client, Client

# Configurações do Supabase (Substitua pelos seus dados do Supabase)
SUPABASE_URL = "https://soqeobghdssvyoivvful.supabase.co"  # URL do seu Supabase
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvcWVvYmdoZHNzdnlvaXZ2ZnVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk1NTQ0NDgsImV4cCI6MjA1NTEzMDQ0OH0.MLTwnh5I3QkbNaRzzXy7lqhl8SFojAN65lT0Sysbwg8"  # Chave de acesso do Supabase

# Criação do cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_insights_yesterday(account_id, access_token):
    """
    Coleta os dados de anúncios do dia anterior para uma conta específica,
    processa os dados, e insere as métricas calculadas no Supabase.
    """
    ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    url_base = (
        f"https://graph.facebook.com/v22.0/act_{account_id}/insights"
        f"?time_increment=1"
        f"&time_range={{\"since\":\"{ontem}\",\"until\":\"{ontem}\"}}"
        f"&level=ad"
        f"&fields=impressions,reach,spend,adset_id,adset_name,ad_id,ad_name,actions"
        f"&action_breakdowns=action_type"
        f"&access_token={access_token}"
    )

    todos_os_dados = []
    url_atual = url_base

    while url_atual:
        resposta = requests.get(url_atual)

        if resposta.status_code != 200:
            print(f"Erro na requisição. Código: {resposta.status_code}")
            print(f"Resposta: {resposta.text}")
            break

        dados = resposta.json()

        if "data" in dados:
            todos_os_dados.extend(dados["data"])

        if "paging" in dados and "next" in dados["paging"]:
            url_atual = dados["paging"]["next"]
            time.sleep(0.005)
        else:
            url_atual = None

    # Processa os dados extraídos
    processed_data = []
    for ad in todos_os_dados:
        # Preenche os dados conforme o formato esperado
        id_conta = account_id  # Agora, estamos usando o parâmetro account_id diretamente
        id_conjunto = str(ad.get("adset_id", ""))
        nome_conjunto = ad.get("adset_name", "Desconhecido")
        id_anuncio = str(ad.get("ad_id", ""))
        nome_anuncio = ad.get("ad_name", "Desconhecido")
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

        # Adiciona os dados processados na lista
        processed_data.append({
            "id_conta": id_conta,
            "id_conjunto": id_conjunto,
            "nome_conjunto": nome_conjunto,
            "id_anuncio": id_anuncio,  # Adiciona o id_anuncio
            "nome_anuncio": nome_anuncio,  # Adiciona o nome_anuncio
            "data_inicio": data_inicio,
            "investimento": investimento,
            "cliques": cliques,
            "leads": leads,
            "cadastro_meta": cadastro_meta,
            "conversas_iniciadas": conversas_iniciadas
        })

    # Insere os dados processados no Supabase
    for registro in processed_data:
        try:
            # Inserção no Supabase
            response = supabase.table("facebook_insights").insert(registro).execute()
            print(f"Dados de {registro['id_conta']} inseridos com sucesso no Supabase!")
        except Exception as e:
            print(f"Erro ao inserir dados de {registro['id_conta']} no Supabase: {e}")

# Função principal
def main():
    # Lê o token de acesso do arquivo
    try:
        with open("novo_token.txt", "r") as f:
            ACCESS_TOKEN = f.read().strip()  # Lê o token de longo prazo do arquivo
    except FileNotFoundError:
        print("Erro: O arquivo 'novo_token.txt' não foi encontrado. Certifique-se de que o token foi renovado.")
        return

    # Lista de todas as contas do Facebook (IDs de contas do Facebook)
    lista_de_contas = [
         "294397361697540",
        "273717500551075",
        "185534306223063",
        "399378954300562",
        "207224937995313",
        "853521859988744",
        "369199774040680",
        "272632814190475",
        "712703422560858",
        "260541305274163",
        "3028903027343475",
        "266116647806266",
        "433757391083398",
        "729097561227405",
        "427999658307455",
        "341867950349467",
        "829731337939484",
        "421556315432981",
        "766843484598389",
        "2650800000000000",
        "2598162083676218",
        "3214406055517297",
        "1213925972283556",
        "198313924760810",
        "1354713388060439",
        "564900578387767",
        "196724701599490",
        "506161170713365",
        "355726933640549",
        "2416446385112004",
        "425250055347651",
        "257122798893050",
        "257917255324718",
        "1758023371040322",
        "582864615970028",
        "559561224946744",
        "977036012752725",
        "264383791293755",
        "2442763915849323",
        "1154015138307321",
        "717825175658793",
        "300036158051894",
        "298926841283208",
        "5434306676675337",
        "652220095673691",
        "1630765270433461",
        "1767837766898401",
        "685333375655758",
        "864255814099011",
        "1424681774358902",
        "511327413610720",
        "2384522878464324",
        "273226450457936",
        "413233799949309",
        "2744202202494865",
        "275686683733706",
        "279434330040473",
        "721165152389246",
        "442051349838768",   # Exemplo de uma conta
        # Adicione mais IDs de contas do Facebook aqui
    ]

    # Para cada conta, executa a coleta de dados
    for account_id in lista_de_contas:
        print(f"\n--- Coletando dados da conta: {account_id} ---")
        fetch_insights_yesterday(account_id, ACCESS_TOKEN)

if __name__ == "__main__":
    main()