import time
import requests
import json

def fetch_all_insights():
    # Substitua este ID de conta e a URL conforme necessário
    account_id = "264383791293755"
    url_inicial = (
        "https://graph.facebook.com/v22.0/act_{account_id}/insights"
        "?time_increment=1&level=ad&fields=impressions%2Creach%2Cspend%2Cadset_id%2Cadset_name%2Cad_id%2Cad_name%2Cactions&action_breakdowns=action_type&access_token=EAARvDNZAUYcEBO4pZCEPUAiWk54zMsCZCkbFhetvWZAhRvhfcG9v6qsHa9a1AyANu0Y3r5ZBr3nUBMvYlujB3kx1iAZCTyjXTRCMqxpRx8Y8KQo8iJgGd99EQkM53UFDQ6QnBofsL4ynWtZBoDiiCVAZBNCIjpwVKhE5cr89tMwDxWL2ojezO5Hxe6Hl6FuSXLDtOPDjd4p78YR9bPWun1zzM5hP2QZDZD"
    ).format(account_id=account_id)

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
    nome_arquivo = f"{account_id}_insights2224.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)

    print(f"Todos os dados foram salvos em '{nome_arquivo}'")

# Se preferir, chame a função diretamente ao rodar o script
if __name__ == "__main__":
    fetch_all_insights()
