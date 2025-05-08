import os
import json

def merge_files(input_folder="f_Json", output_folder="Versao_final"):
    # Cria o diretório de saída se não existir
    os.makedirs(output_folder, exist_ok=True)
    
    # Lista todos os arquivos na pasta de entrada
    files_to_merge = [f for f in os.listdir(input_folder) if f.endswith(".json")]
    
    all_data = []
    
    # Carrega todos os dados dos arquivos na pasta
    for file in sorted(files_to_merge):
        file_path = os.path.join(input_folder, file)

        # Carrega os dados do arquivo
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    
    # Definindo o nome do arquivo de saída com base no ID fixo
    output_file = os.path.join(output_folder, "198313924760810_complete.json")
    
    # Salva os dados mesclados em um único arquivo
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Arquivo mesclado salvo em: {output_file}")

if __name__ == "__main__":
    merge_files()
