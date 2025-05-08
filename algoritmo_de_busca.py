import os
import json
 
def move_files(account_ids, input_folder="json_atualizado", output_folder="aqui"):
    """
    Função que move arquivos da pasta 'input_folder' para 'output_folder' para cada conta na lista 'account_ids'.
    Os arquivos devem começar com o 'id' da conta.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Percorre cada ID de conta da lista fornecida
    for account_id in account_ids:
        print(f"🔄 Processando arquivos para a conta {account_id}...")
        
        # Filtra os arquivos que começam com o ID da conta
        files_to_process = [f for f in os.listdir(input_folder) if f.startswith(str(account_id)) and f.endswith(".json")]
        
        # Processa os arquivos encontrados
        for file in files_to_process:
            print(f"Verificando arquivo: {file}")  # Log para depuração
            
            # Move o arquivo para a pasta de saída
            input_file_path = os.path.join(input_folder, file)
            output_file_path = os.path.join(output_folder, file)
            os.rename(input_file_path, output_file_path)
            print(f"✅ Arquivo {file} movido para a pasta {output_folder}.")

def merge_with_completos(account_id, input_folder_json="Json_atualizado", input_folder_completos="Completos", output_folder="Completos"):
    """
    Função que mescla os arquivos de uma conta específica da pasta 'Json_atualizado' com os arquivos da pasta 'Completos',
    e salva o arquivo mesclado na pasta 'Completos'.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Filtra os arquivos que começam com o ID da conta na pasta Json_atualizado
    files_to_merge_json = [f for f in os.listdir(input_folder_json) if f.startswith(str(account_id)) and f.endswith(".json")]
    
    # Filtra os arquivos que começam com o ID da conta na pasta Completos
    files_to_merge_completos = [f for f in os.listdir(input_folder_completos) if f.startswith(str(account_id)) and f.endswith(".json")]
    
    all_data = []
    
    # Carrega e mescla os dados dos arquivos encontrados na pasta Json_atualizado
    for file in files_to_merge_json:
        file_path = os.path.join(input_folder_json, file)

        # Carrega os dados do arquivo
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    
    # Carrega e mescla os dados dos arquivos encontrados na pasta Completos
    for file in files_to_merge_completos:
        file_path = os.path.join(input_folder_completos, file)

        # Carrega os dados do arquivo
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    
    # Define o nome do arquivo de saída com base no ID da conta
    output_file = os.path.join(output_folder, f"{account_id}_complete.json")
    
    # Salva os dados mesclados em um único arquivo
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Arquivo mesclado para a conta {account_id} salvo em: {output_file}")

def merge_final(account_id, input_folder_completos="Completos", output_folder="Completos"):
    """
    Função que mescla os arquivos da pasta 'Completos' com os arquivos já mesclados.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Filtra os arquivos que começam com o ID da conta na pasta Completos
    files_to_merge_completos = [f for f in os.listdir(input_folder_completos) if f.startswith(str(account_id)) and f.endswith(".json")]
    
    all_data = []
    
    # Carrega e mescla os dados dos arquivos encontrados na pasta Completos
    for file in files_to_merge_completos:
        file_path = os.path.join(input_folder_completos, file)

        # Carrega os dados do arquivo
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    
    # Define o nome do arquivo de saída com base no ID da conta
    output_file = os.path.join(output_folder, f"{account_id}_complete.json")
    
    # Salva os dados mesclados em um único arquivo
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Arquivo final mesclado para a conta {account_id} salvo em: {output_file}")

def process_all(account_ids, input_folder_move="json_atualizado", output_folder_move="aqui", output_folder_merge="Completos"):
    """
    Função que executa tanto a movimentação quanto a mesclagem dos arquivos.
    """
    # Move os arquivos para a pasta 'aqui'
    move_files(account_ids, input_folder_move, output_folder_move)
    
    # Mescla os arquivos de cada conta com os arquivos da pasta 'Completos'
    for account_id in account_ids:
        # Primeiro, mescla com os arquivos da pasta 'Json_atualizado'
        merge_with_completos(account_id, output_folder_move, output_folder_merge, output_folder_merge)
        # Depois, mescla com os arquivos da pasta 'Completos'
        merge_final(account_id, output_folder_merge, output_folder_merge)

if __name__ == "__main__":
    # Lista de IDs de contas para processar
    account_ids = [
        "185534306223063", "196724701599490", "198313924760810", "257122798893050", 
        "257917255324718", "260541305274163", "279434330040473", "300036158051894", 
        "369199774040680", "421556315432981", "425250055347651", "564900578387767", 
        "853521859988744", "1424681774358902", "1630765270433461", "1767837766898401", 
        "2384522878464324", "2442763915849323", "2650800000000000", "5434306676675337", "207224937995313"
    ]
    
    # Executa o processo completo de mover e mesclar arquivos
    process_all(account_ids)
