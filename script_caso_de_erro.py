import time
import requests
import json

def fetch_all_insights():
    # Substitua este ID de conta e a URL conforme necessário
    account_id = "341867950349467"
    url_inicial = (
        "https://graph.facebook.com/v22.0/act_341867950349467/insights?time_increment=1&time_range={since:2022-06-01,until:2024-12-31}&%20level=ad&%20fields=impressions,account_id,reach,spend,adset_id,adset_name,ad_id,ad_name,actions&%20action_breakdowns=action_type&access_token=EAARvDNZAUYcEBO1iqEkZB21hD1TemOA6tpwjvcjXnZBk4UJjhHpzeger6J0H1QIha3RvZBjFWmVSFcqCEWRlbyR3Iav3NxVLVPlcRQ8ZChQmqpnpo00dCE9Qd9HNd8tZB8GCHqg2jhvqtassrYxO9dHSXLOIVTIdYWLSb05h8W0J8zwBfScLS7o1FXEoSreU23uu22Y8gV" # Alterar AQUI com o último After ID que aparecer na URL em que a requisição deu erro
    )

    # Lista para armazenar todos os registros de todas as páginas
    todos_os_dados = []

    # URL de requisição atual (iniciando pela url_inicial)
    url_atual = url_inicial

    while url_atual:
        print(f"Fazendo requisição para: {url_atual}")
        resposta = requests.get(url_atual)
        
        if resposta.status_code != 200:
            print(f"Erro na requisição. Código: {resposta.status_code}")
            print(f"Resposta: {resposta.text}")
            break

        # Carrega os dados como JSON
        dados = resposta.json()

        # Armazena a lista de dados da página atual
        # O campo "data" é onde o Facebook Ads Insights retorna as informações
        if "data" in dados:
            # Se "data" for uma lista, adicionamos todos
            todos_os_dados.extend(dados["data"])
        else:
            print("Nenhum campo 'data' encontrado nessa resposta. Encerrando.")
            break

        # Verifica se existe a próxima página
        # Normalmente, a estrutura é "paging": { "next": "...url..." }
        if "paging" in dados and "next" in dados["paging"]:
            url_atual = dados["paging"]["next"]
            
            # Espera 5 ms (0.005 segundos) para evitar problemas de rate limit
            time.sleep(0.005)
        else:
            # Não há próxima página, então finaliza o loop
            url_atual = None

    # Salva todos os dados em um único arquivo JSON
    nome_arquivo = f"{account_id}_insights2224_parte2.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)

    print(f"Todos os dados foram salvos em '{nome_arquivo}'")

# Se preferir, chame a função diretamente ao rodar o script
if __name__ == "__main__":
    fetch_all_insights()