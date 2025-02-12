import time
import requests
import json
import urllib.parse  # Import necessário para formatar corretamente a URL

def fetch_all_insights():
    # Substitua este ID de conta e a URL conforme necessário
    account_id = "369199774040680"
    
    # Definição do time_range no formato correto
    time_range = json.dumps({"since": "2022-06-01", "until": "2022-07-31"})
    
    # Codificação correta do time_range para a URL
    encoded_time_range = urllib.parse.quote(time_range)

    # Construção da URL corrigida
    url_inicial = (
        f"https://graph.facebook.com/v22.0/act_{account_id}/insights"
        f"?time_increment=1&time_range={encoded_time_range}&level=ad&fields=impressions,%20account_id,reach,spend,adset_id,adset_name,ad_id,ad_name,actions&action_breakdowns=action_type&access_token=EAAWU1dRzrNUBOxJleckdPvIDBRZAVyV6hkKhxBlLFK1SXsLlv9VZBlQ1f2W6l77z8XEDoaPW57CgVpvoVDZAUGAJSlZCRPMEU6E4YZAfTVVxYXwd6oR6kUKLfkugWylZAUH1PaGRgvA1rfCsrrPHX72ljO3slwYjkYlCgIwcFeU1v9PSQ2FZCqak73ZBDPZALrJ5y5B7JIYdZCFE87gRCBM1UJe4A6GQZDZD"
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
        if "data" in dados and isinstance(dados["data"], list):
            # Se "data" for uma lista, adicionamos todos
            todos_os_dados.extend(dados["data"])
        else:
            print("Nenhum campo 'data' encontrado nessa resposta. Encerrando.")
            break

        # Verifica se existe a próxima página
        if "paging" in dados and "next" in dados["paging"]:
            url_atual = dados["paging"]["next"]
            
            # Espera 5 ms (0.005 segundos) para evitar problemas de rate limit
            time.sleep(0.005)
        else:
            url_atual = None  # Finaliza o loop

    # Salva todos os dados em um único arquivo JSON
    nome_arquivo = f"{account_id}_insights2224_parte1.json"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)

    print(f"✅ Todos os dados foram salvos em '{nome_arquivo}'")

# Se preferir, chame a função diretamente ao rodar o script
if __name__ == "__main__":
    fetch_all_insights()
