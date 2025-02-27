import requests
import json
import time
from datetime import datetime, timedelta

def fetch_insights_yesterday(account_id, access_token):
    """
    Coleta os dados de anúncios do dia anterior para uma conta específica,
    lida com a paginação e salva os resultados em um único arquivo JSON.
    """

    # 1. Identificar a data de ontem no formato YYYY-MM-DD
    ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # 2. Montar a URL de requisição para o dia de ontem
    url_base = (
        f"https://graph.facebook.com/v22.0/act_{account_id}/insights?time_increment=1"
        f"&time_range={{\"since\":\"{ontem}\",\"until\":\"{ontem}\"}}"
        f"&level=ad&fields=impressions,reach,spend,adset_id,adset_name,ad_id,ad_name,actions&action_breakdowns=action_type"
        f"&access_token={access_token}"
    )

    # Lista que irá conter todos os registros de todas as páginas
    todos_os_dados = []

    # URL inicial para começar a requisição
    url_atual = url_base

    while url_atual:
        print(f"Fazendo requisição para: {url_atual}")
        resposta = requests.get(url_atual)
        
        if resposta.status_code != 200:
            print(f"Erro na requisição. Código: {resposta.status_code}")
            print(f"Resposta: {resposta.text}")
            break

        # Carrega os dados JSON
        dados = resposta.json()

        # Verifica se a resposta possui o campo "data"
        if "data" in dados:
            # "data" normalmente é uma lista de objetos de insights
            todos_os_dados.extend(dados["data"])
        else:
            print("Nenhum campo 'data' encontrado nessa resposta. Encerrando.")
            break

        # 3. Verificar se existe próximo link em "paging.next"
        #    (em vez de "pagination", a Graph API usa "paging")
        if "paging" in dados and "next" in dados["paging"]:
            url_atual = dados["paging"]["next"]
            
            # Espera 5 ms antes de fazer a próxima requisição
            time.sleep(0.005)
        else:
            # Não há próxima página
            url_atual = None

    # Por fim, salva tudo em um único arquivo JSON
    nome_arquivo = f"{account_id}_insights2224.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)

    print(f"Coleta finalizada! Dados salvos em '{nome_arquivo}'.")


if __name__ == "__main__":
    # Exemplo de uso:
    # Se tiver apenas uma conta, basta chamar a função para aquela conta.
    # Caso tenha várias, repita para cada ID.

    # Defina seu token de acesso (Access Token do Meta)
    ACCESS_TOKEN = "EAAWU1dRzrNUBOw6G0Or2CxCBthZAhMHTnZAK8S0F6GGcUWkrTZB5mKVfKK9YCx2CATF1EybNhhuKZBsL19zDp7gUID7VmHfO5WWlQTjnOgWSosotAX8yZAoZCTI7L0DllqcYOrZC1WuinoMmIoMLXam4LjFKyrqRZB4Bzl9S2xry1fKArOiyXGlCFKmZCZAQjBiEYA23BEGSFYl0ljfV5cxLRqEzJD8OYE0eMqOUwZD"

    # Caso você tenha apenas UMA conta:
    # fetch_insights_yesterday("1234567890", ACCESS_TOKEN)

    # Caso tenha VÁRIAS contas, itere sobre elas:
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
        "442051349838768"
    ]

    for account_id in lista_de_contas:
        print(f"\n--- Coletando dados da conta: {account_id} ---")
        fetch_insights_yesterday(account_id, ACCESS_TOKEN)


