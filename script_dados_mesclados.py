import os
import json

# Caminho da pasta com os arquivos JSON
pasta_json = r"C:\Users\Vini\OneDrive\Documents\VSCODE\sereducacional\341867950349467"  # Caminho da sua pasta
arquivo_saida = "341867950349467_completeinsights2224.json"  # Nome do arquivo consolidado

# Lista para armazenar todos os dados
dados_mesclados = []

# Iterar sobre os arquivos na pasta
for nome_arquivo in os.listdir(pasta_json):
    if nome_arquivo.endswith(".json"):  # Garantir que são arquivos JSON
        caminho_arquivo = os.path.join(pasta_json, nome_arquivo)
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)  # Carregar o conteúdo JSON
                # Verificar se o conteúdo é uma lista ou um dicionário
                if isinstance(dados, list):
                    dados_mesclados.extend(dados)  # Adicionar listas diretamente
                else:
                    dados_mesclados.append(dados)  # Adicionar dicionários
            except json.JSONDecodeError:
                print(f"Erro ao carregar o arquivo: {nome_arquivo}")

# Salvar os dados mesclados em um único arquivo JSON
caminho_saida = os.path.join(pasta_json, arquivo_saida)
with open(caminho_saida, "w", encoding="utf-8") as f:
    json.dump(dados_mesclados, f, indent=4, ensure_ascii=False)

print(f"Arquivos mesclados e salvos em '{caminho_saida}'")
