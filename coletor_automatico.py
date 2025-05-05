import time
import requests
import json
import urllib.parse
from datetime import datetime, timedelta
import os

def fetch_insights_range(account_id, access_token, start_date_str, end_date_str, pasta_saida="New_Json"):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    while start_date <= end_date:
        since = start_date.strftime("%Y-%m-%d")
        until = since

        time_range = json.dumps({"since": since, "until": until})
        encoded_time_range = urllib.parse.quote(time_range)

        url = (
            f"https://graph.facebook.com/v22.0/act_{account_id}/insights"
            f"?time_increment=1&time_range={encoded_time_range}&level=ad"
            f"&fields=impressions,account_id,reach,spend,adset_id,adset_name,ad_id,ad_name,actions"
            f"&action_breakdowns=action_type&access_token={access_token}"
        )

        print(f"🔄 Conta {account_id} – Coletando {since}...")

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
            nome_arquivo = os.path.join(pasta_saida, f"{account_id}_insights_{since}.json")
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)
            print(f"✅ Salvo: {nome_arquivo}")
        else:
            print(f"⚠️ Sem dados para {account_id} em {since}.")

        start_date += timedelta(days=1)


if __name__ == "__main__":
    ACCESS_TOKEN = "EAANWRqx9Ex8BO8Lfn23xuzk18Mh5wCjF1moS2ZA8B0FAzKBZCBYzuNBUGUCfwfkxiqKZBBdtNEAH3ZAxQH2NSfg7hOq0TQHe72ME9AMcrKRr6qgGuyCfuvw5LWhQISvGouEcoPtkwaasZChSiylYspZCwdOZAkREZCPJFXAz3lpMlG3mTIfmGT8QxIls3gAqvYHDUcsNyEZBF"

    # Lista completa de contas de anúncios
    lista_de_contas = [
        "294397361697540", "273717500551075", "185534306223063", "399378954300562", "207224937995313",
        "853521859988744", "369199774040680", "272632814190475", "712703422560858", "260541305274163",
        "3028903027343475", "266116647806266", "433757391083398", "729097561227405", "427999658307455",
        "341867950349467", "829731337939484", "421556315432981", "766843484598389", "2650800000000000",
        "2598162083676218", "3214406055517297", "1213925972283556", "198313924760810", "1354713388060439",
        "564900578387767", "196724701599490", "506161170713365", "355726933640549", "2416446385112004",
        "425250055347651", "257122798893050", "257917255324718", "1758023371040322", "582864615970028",
        "559561224946744", "977036012752725", "264383791293755", "2442763915849323", "1154015138307321",
        "717825175658793", "300036158051894", "298926841283208", "5434306676675337", "652220095673691",
        "1630765270433461", "1767837766898401", "685333375655758", "864255814099011", "1424681774358902",
        "511327413610720", "2384522878464324", "273226450457936", "413233799949309", "2744202202494865",
        "275686683733706", "279434330040473", "721165152389246", "442051349838768"
    ]

    # Define o intervalo desejado
    DATA_INICIO = "2025-02-27"
    DATA_FIM = "2025-05-05"

    for account_id in lista_de_contas:
        print(f"\n🟦 Iniciando coleta para conta: {account_id}")
        fetch_insights_range(account_id, ACCESS_TOKEN, DATA_INICIO, DATA_FIM)
