import time
import requests
import json
import urllib.parse
from datetime import datetime, timedelta
import os
 
def fetch_insights_range(account_id, access_token, start_date_str, end_date_str, pasta_saida="Megerd_Json"):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    while start_date <= end_date:
        # Define o final do mês (pode ser o próprio último dia do mês)
        next_month = start_date.replace(day=28) + timedelta(days=4)  # Vai para o próximo mês
        end_of_month = next_month - timedelta(days=next_month.day)  # Último dia do mês atual

        # Caso o final do mês ultrapasse a data final definida, ajusta
        if end_of_month > end_date:
            end_of_month = end_date

        # Formata as datas
        since = start_date.strftime("%Y-%m-%d")
        until = end_of_month.strftime("%Y-%m-%d")

        time_range = json.dumps({"since": since, "until": until})
        encoded_time_range = urllib.parse.quote(time_range)

        url = (
            f"https://graph.facebook.com/v22.0/act_{account_id}/insights"
            f"?time_increment=1&time_range={encoded_time_range}&level=ad"
            f"&fields=impressions,account_id,reach,spend,adset_id,adset_name,ad_id,ad_name,actions"
            f"&action_breakdowns=action_type&access_token={access_token}"
        )

        print(f"🔄 Conta {account_id} – Coletando de {since} até {until}...")

        todos_os_dados = []
        url_atual = url

        while url_atual:
            try:
                resposta = requests.get(url_atual)
                if resposta.status_code != 200:
                    print(f"❌ Erro {resposta.status_code} - {resposta.text}")
                    break

                dados = resposta.json()
                todos_os_dados.extend(dados.get("data", []))

                if "paging" in dados and "next" in dados["paging"]:
                    url_atual = dados["paging"]["next"]
                    time.sleep(0.2)
                else:
                    break
            except Exception as e:
                print(f"⚠️ Erro ao processar requisição: {e}")
                break

        # Criação da pasta, se não existir
        os.makedirs(pasta_saida, exist_ok=True)

        if todos_os_dados:
            nome_arquivo = os.path.join(pasta_saida, f"{account_id}_insights_{since}_to_{until}.json")
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)
            print(f"✅ Salvo: {nome_arquivo}")
        else:
            print(f"⚠️ Sem dados para {account_id} de {since} até {until}.")

        # Avança para o próximo mês
        start_date = end_of_month + timedelta(days=1)

if __name__ == "__main__":
    ACCESS_TOKEN = "EAANWRqx9Ex8BOZBEufWbayTjX3sy9StKOsGjZB6PBO8SFah2dVaK8orKcbLJnZCwWxymymHvzuHBlNUq9A1gRZAYLxF2Yid6DepOZBGeuAPC3qR3diDnpeU1B3Poj1NeNQMWwWqjfFahqaUzZCEzZAAGrub3dQIje1G4SR3Fhj3F5HuBlxDlAVVB4bvAiZB53zaempZBm3nMz"

    # Lista completa de contas de anúncios
    lista_de_contas = [
        "185534306223063", "198313924760810", "196724701599490"
    ]

    # Define o intervalo desejado
    DATA_INICIO = "2025-02-06"
    DATA_FIM = "2025-05-06"

    for account_id in lista_de_contas:
        print(f"\n🟦 Iniciando coleta para conta: {account_id}")
        fetch_insights_range(account_id, ACCESS_TOKEN, DATA_INICIO, DATA_FIM)
