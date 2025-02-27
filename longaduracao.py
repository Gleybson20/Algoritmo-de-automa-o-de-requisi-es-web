import requests
import os

def renovar_token():
    # Substitua as credenciais diretamente na URL
    client_id = "939286471709471"  # ID do aplicativo
    client_secret = "c01a0a4af5cb01c67e1daac7c6dc8882"  # Chave secreta do aplicativo
    access_token = "EAANWRqx9Ex8BO4vVdkebZABa2VxOfMisNif2AFpYobWDXlerw7K5W50DWmZBDjYV0ZANpv6AfO5dfuRjv89KGhPUZAP5ijC1N2FjTZCdHVoI84OD6lpV28hNQknoFTQjIGK3pHEAHIQNC1ZBM0cJanCekSIhDnaLDlOPIockKmc6rOuJ7ftPutUNz5xJ82WpXW7xzgz1Ej"  # Token de acesso verdadeiro

    # Verifica o diretório atual para garantir que o arquivo será salvo corretamente
    print("Diretório atual:", os.getcwd())
    
    # Inicializa o caminho do arquivo onde o token será salvo
    file_path = os.path.join(os.getcwd(), "novo_token.txt")  # Caminho no diretório atual

    # Caso o token não esteja definido como variável de ambiente, tente ler do arquivo
    if not access_token:
        try:
            with open(file_path, "r") as f:
                access_token = f.read().strip()  # Lê e remove qualquer espaço extra ou quebras de linha
            print(f"Token lido do arquivo {file_path}")
        except FileNotFoundError:
            print(f"Erro: O arquivo '{file_path}' não foi encontrado. Certifique-se de que o token foi renovado.")
            return

    # Verifique se o token de acesso é válido
    if not access_token:
        print("Erro: Nenhum token de acesso encontrado!")
        return

    # URL para renovar o token de acesso
    url = f"https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id={client_id}&client_secret={client_secret}&fb_exchange_token={access_token}"

    # Realiza a requisição GET para renovar o token
    response = requests.get(url)

    if response.status_code == 200:
        try:
            novo_token = response.json()['access_token']
            print(f"Novo token de longa duração: {novo_token}")
            
            # Salva o novo token de longa duração em um arquivo
            with open(file_path, "w") as f:
                f.write(novo_token)
            print(f"Novo token salvo no arquivo '{file_path}'.")
            
            # Atualiza a variável de ambiente com o novo token
            os.environ["FACEBOOK_ACCESS_TOKEN"] = novo_token
        except KeyError:
            print("Erro: A resposta da API não contém um token de acesso.")
    else:
        print("Erro ao renovar o token:", response.json())

# Testar a renovação do token
renovar_token()
