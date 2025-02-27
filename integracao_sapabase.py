from supabase import create_client, Client
import requests
import json
import os
from datetime import datetime, timedelta

# Configuração do Supabase
SUPABASE_URL = "https://seusupabaseurl.supabase.co"
SUPABASE_KEY = "sua-chave-secreta"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuração do Meta Ads
ACCESS_TOKEN = "seu-token-do-facebook"
ACCOUNTS = [
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
        "442051349838768"
    ]  # Lista de contas de anúncio

def fetch_insights_yesterday(account_id):
    """
    Coleta os dados de anúncios do dia anterior para uma conta específica e retorna os resultados.
    """
    ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    url = (
        f"https://graph.facebook.com/v21.0/act_{account_id}/insights"
        f"?time_increment=1&time_range={{\"since\":\"{ontem}\",\"until\":\"{ontem}\"}}&level=ad&fields=impressions,reach,spend,adset_id,adset_name,ad_id,ad_name,actions"
        f"&access_token={ACCESS_TOKEN}"
    )
    response = requests.get(url)
    return response.json().get("data", [])

def salvar_dados_no_supabase(dados):
    """
    Insere ou atualiza os dados no Supabase.
    """
    for registro in dados:
        response = supabase.table("unidades_metricas").upsert(registro).execute()
        print("Inserido:", response.data)

def processar_todas_as_contas():
    """
    Executa a coleta e armazenamento dos dados para todas as contas configuradas.
    """
    for account in ACCOUNTS:
        dados = fetch_insights_yesterday(account)
        if dados:
            salvar_dados_no_supabase(dados)

if __name__ == "__main__":
    processar_todas_as_contas()