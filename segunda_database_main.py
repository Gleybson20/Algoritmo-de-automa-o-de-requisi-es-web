import pandas as pd
from segunda_database import second_load_json, second_process_json_data

# Caminho do arquivo JSON
input_file = "insights2224.json"
output_file = "second_processed_data.xlsx"

# Carrega os dados
data = second_load_json(input_file)

# Processa os dados
processed_data = second_process_json_data(data)
df = pd.DataFrame(processed_data)

# Salva os dados no Excel
df.to_excel(output_file, index=False)

print(f"Processamento concluído e planilha gerada: {output_file}")
