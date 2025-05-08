import os
import json
import re
from datetime import datetime
 
def process_account_files(account_id, input_folder="Megerd_Json", output_folder="f_Json"):
    # Cria o diretório de saída se não existir
    os.makedirs(output_folder, exist_ok=True)
    
    # Filtra os arquivos que seguem o formato correto
    files_to_process = [f for f in os.listdir(input_folder) if f.startswith(str(account_id)) and f.endswith(".json")]

    # Define a faixa de datas
    start_date = datetime.strptime("2025-02-27", "%Y-%m-%d")
    end_date = datetime.strptime("2025-05-05", "%Y-%m-%d")
    
    # Processa os arquivos encontrados
    for file in files_to_process:
        # Verifica se o arquivo corresponde ao formato: <id>_insights_YYYY-MM-DD.json
        pattern = r"^" + re.escape(str(account_id)) + r"_insights_(\d{4}-\d{2}-\d{2})\.json$"
        match = re.match(pattern, file)
        
        if match:
            # Extrai a data do nome do arquivo
            file_date_str = match.group(1)
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            
            # Verifica se a data está dentro do intervalo permitido
            if start_date <= file_date <= end_date:
                # Move o arquivo para a pasta de saída
                input_file_path = os.path.join(input_folder, file)
                output_file_path = os.path.join(output_folder, file)
                
                # Move o arquivo para o diretório de saída
                os.rename(input_file_path, output_file_path)
                print(f"✅ Arquivo {file} movido para a pasta f_Json.")
            else:
                print(f"⚠️ Arquivo {file} tem data fora do intervalo e foi ignorado.")
        else:
            print(f"⚠️ Arquivo {file} não corresponde ao formato esperado e foi ignorado.")

def process_single_account(account_id, input_folder="Megerd_Json", output_folder="f_Json"):
    print(f"\n🔄 Iniciando o processamento dos arquivos para a conta {account_id}...")
    process_account_files(account_id, input_folder, output_folder)

if __name__ == "__main__":
    # Altere o account_id para o que você deseja processar
    account_id = "196724701599490" 
    process_single_account(account_id)
