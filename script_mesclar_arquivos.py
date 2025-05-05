import os
import json
from datetime import datetime

def merge_account_data(account_id, input_folder="New_Json", output_folder="Merged_Json"):
    # Cria o diretório de saída se não existir
    os.makedirs(output_folder, exist_ok=True)
    
    # Filtra os arquivos que começam com o ID da conta
    files_to_merge = [f for f in os.listdir(input_folder) if f.startswith(str(account_id))]
    
    all_data = []
    
    # Carrega todos os dados dos arquivos que correspondem ao ID da conta
    for file in files_to_merge:
        with open(os.path.join(input_folder, file), "r", encoding="utf-8") as f:
            data = json.load(f)
            all_data.extend(data)
    
    # Ordena os dados pela data (assumindo que cada item tenha um campo de data chamado 'date')
    all_data.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))
    
    # Salva os dados mesclados em um único arquivo
    output_file = os.path.join(output_folder, f"{account_id}_merged.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Arquivo mesclado para a conta {account_id} salvo em: {output_file}")

def merge_all_accounts(input_folder="New_Json", output_folder="Merged_Json"):
    # Lista de IDs de contas (como mencionado no seu código)
    account_ids = [
        "294397361697540", "273717500551075", "185534306223063", "399378954300562", "207224937995313",
        "853521859988744", "369199774040680", "272632814190475", "712703422560858", "260541305274163",
        "3028903027343475", "266116647806266", "433757391083398", "729097561227405", "427999658307455",
        "341867950349467", "829731337939484", "421556315432981", "766843484598389", "2650800000000000",
        "2598162083676218", "3214406055517297", "1213925972283556", "198313924760810", "1354713388060439",
        "564900578387767", "196724701599490", "506161170713365", "355726933640549", "2416446385112004",
        "425250055347651", "257122798893050", "257917255324718", "1758023371040322", "582864615970028",
        "559561224946744", "977036012752725", "264383791293755", "2442763915849323", "1154015138307321",
        "717825175658793", "300036158051894", "298926841283208", "5434306676675337", "652220095673691",
        "1630765270433461", "1767837766898401", "685333375655758", "864255814099011", "1424681774358902",
        "511327413610720", "2384522878464324", "273226450457936", "413233799949309", "2744202202494865",
        "275686683733706", "279434330040473", "721165152389246", "442051349838768"
    ]
    
    # Mescla os arquivos para cada ID de conta
    for account_id in account_ids:
        print(f"\n🔄 Iniciando a mesclagem dos dados para a conta {account_id}...")
        merge_account_data(account_id, input_folder, output_folder)

if __name__ == "__main__":
    merge_all_accounts()
