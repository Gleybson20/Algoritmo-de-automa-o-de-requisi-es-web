import os
import time
import requests
import json

# Definições
ACCESS_TOKEN = os.getenv("EAARvDNZAUYcEBO1iqEkZB21hD1TemOA6tpwjvcjXnZBk4UJjhHpzeger6J0H1QIha3RvZBjFWmVSFcqCEWRlbyR3Iav3NxVLVPlcRQ8ZChQmqpnpo00dCE9Qd9HNd8tZB8GCHqg2jhvqtassrYxO9dHSXLOIVTIdYWLSb05h8W0J8zwBfScLS7o1FXEoSreU23uu22Y8gV")
ACCOUNT_ID = "341867950349467"
MAX_RETRIES = 3
RATE_LIMIT_SLEEP = 1

# Períodos para a requisição
PERIODOS = [
    {"since": "2022-06-01", "until": "2022-12-31"},
    {"since": "2023-01-01", "until": "2023-12-31"},
    {"since": "2024-01-01", "until": "2024-12-31"}
]

def fetch_insights_for_period(time_range):
    """ Faz requisições para um período específico e retorna os dados coletados. """
    url_base = f"https://graph.facebook.com/v22.0/act_{ACCOUNT_ID}/insights"

    params = {
        "?time_increment=1&time_range={since:2022-06-01,until:2024-12-31}&%20level=ad&%20fields=impressions,account_id,reach,spend,adset_id,adset_name,ad_id,ad_name,actions&%20action_breakdowns=action_type&access_token=EAARvDNZAUYcEBO1iqEkZB21hD1TemOA6tpwjvcjXnZBk4UJjhHpzeger6J0H1QIha3RvZBjFWmVSFcqCEWRlbyR3Iav3NxVLVPlcRQ8ZChQmqpnpo00dCE9Qd9HNd8tZB8GCHqg2jhvqtassrYxO9dHSXLOIVTIdYWLSb05h8W0J8zwBfScLS7o1FXEoSreU23uu22Y8gV"
    }

    todos_os_dados = []
    url_atual = url_base

    while url_atual:
        for tentativa in range(MAX_RETRIES):
            try:
                print(f"📡 Fazendo requisição para: {url_atual} - Período {time_range}")
                resposta = requests.get(url_atual, params=params, timeout=10)
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    break  # Sai do loop de tentativas se for bem-sucedido
                else:
                    print(f"⚠ Tentativa {tentativa+1}/{MAX_RETRIES} - Erro {resposta.status_code}: {resposta.text}")
                    time.sleep(2 ** tentativa)
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro na conexão: {e}")
                time.sleep(2 ** tentativa)
        else:
            print("🚨 Falha após várias tentativas. Encerrando o processo para este período.")
            return []

        if "data" in dados:
            todos_os_dados.extend(dados["data"])
        else:
            print("⚠ Nenhum campo 'data' encontrado nessa resposta. Encerrando.")
            break

        # Paginação
        url_atual = dados.get("paging", {}).get("next")

        if url_atual:
            time.sleep(RATE_LIMIT_SLEEP)

    return todos_os_dados

def fetch_all_insights():
    """ Coleta dados para todos os períodos definidos e salva em arquivos JSON separados. """
    for periodo in PERIODOS:
        print(f"\n🔍 Coletando dados para o período {periodo['since']} até {periodo['until']}...")
        dados_periodo = fetch_insights_for_period(periodo)

        if dados_periodo:
            nome_arquivo = f"{ACCOUNT_ID}_insights_{periodo['since']}_to_{periodo['until']}.json"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados_periodo, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Dados do período {periodo['since']} - {periodo['until']} salvos em '{nome_arquivo}'\n")
        else:
            print(f"⚠ Nenhum dado encontrado para o período {periodo['since']} - {periodo['until']}.")

# Executar a função ao rodar o script
if __name__ == "__main__":
    fetch_all_insights()
