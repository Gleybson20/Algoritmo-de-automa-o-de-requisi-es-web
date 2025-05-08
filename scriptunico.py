import time
import requests
import json
 
def fetch_all_insights():
    account_id = "341867950349467"

    url_inicial = (
        "https://graph.facebook.com/v22.0/act_341867950349467/insights?time_increment=1&time_range=%7B%22since%22%3A%222022-06-01%22%2C%22until%22%3A%222024-31-12%22%7D&level=ad&fields=impressions%2C%20account_id%2Creach%2Cspend%2Cadset_id%2Cadset_name%2Cad_id%2Cad_name%2Cactions&action_breakdowns=action_type&access_token=EAARvDNZAUYcEBOZC3TTtos00gJdiU0QaM7ZAieXPLPjkRnMlLCeBUsXUx170yOzgc0q6WwWl1RncKlVB4bWYNxRouZCQpgom9nnL906QB92M0xch2YnwDxMKX9y4kx5mc3oqUZBOhpyrNJ2kagptDbdSu6sjdm0QRhKadRJFnoL94aQrMjQZA5c1nkNjFxJNFz6bIfcqHgVvPh66XZCYnrHYlFZAiAZDZD"
    ).format(account_id=account_id)

    todos_os_dados = []
    url_atual = url_inicial

    # Nome do arquivo final (único)
    nome_arquivo = f"{account_id}_insights_completo.json"

    while url_atual:
        print(f"Fazendo requisição para: {url_atual}")
        
        # Tentativas de requisição (retry) se erro temporário
        num_tentativas = 3
        sucesso_na_requisicao = False
        
        for tentativa in range(num_tentativas):
            resposta = requests.get(url_atual)
            
            if resposta.status_code == 200:
                # Sucesso!
                sucesso_na_requisicao = True
                break
            else:
                print(f"Erro na requisição (tentativa {tentativa+1} de {num_tentativas}).")
                print(f"Código: {resposta.status_code}")
                print(f"Resposta: {resposta.text}")
                
                # Se for erro 5xx (ex: 500, 503), vale a pena tentar novamente
                # Se for erro 4xx (ex: 400, 403, 404), geralmente é fatal
                # Mas vamos tentar novamente só se for >= 500
                if resposta.status_code >= 500:
                    # Espera alguns segundos e tenta de novo
                    time.sleep(2)
                else:
                    # É erro "fatal" (4xx) ou outro -> não adianta tentar de novo
                    break
        
        if not sucesso_na_requisicao:
            # Chegamos aqui se as tentativas não deram certo
            print("Não foi possível continuar devido a erros. Salvando dados parciais e encerrando.")
            break

        # Se chegou aqui, 'resposta' é 200 e 'resposta.json()' funciona
        dados = resposta.json()

        # Armazena a lista de dados da página atual
        if "data" in dados and isinstance(dados["data"], list):
            todos_os_dados.extend(dados["data"])
        else:
            print("Nenhum campo 'data' encontrado nessa resposta. Encerrando.")
            break

        # Verifica se existe próxima página
        if "paging" in dados and "next" in dados["paging"]:
            url_atual = dados["paging"]["next"]
            # Espera 5 ms (poderia aumentar se tiver rate limit frequente)
            time.sleep(0.005)
        else:
            print("Não há próxima página. Coleta finalizada.")
            url_atual = None

    # Se chegamos ao fim (sucesso ou não), salvamos TUDO que foi obtido até agora:
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(todos_os_dados, f, indent=4, ensure_ascii=False)

    print(f"Dados salvos em '{nome_arquivo}' (podem ser parciais, caso tenha ocorrido erro).")

if __name__ == "__main__":
    fetch_all_insights()
