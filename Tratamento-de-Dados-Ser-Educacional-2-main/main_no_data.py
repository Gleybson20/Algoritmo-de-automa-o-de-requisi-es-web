import pandas as pd
from base_no_data import load_json, process_json_data, create_dataframe

# Caminho do arquivo JSON
input_file = "729097561227405_insights2224.json"
output_file = "processed_data_caruaru.xlsx"

# Carrega os dados
data = load_json(input_file)

# Processa os dados
processed_data = process_json_data(data)
df = create_dataframe(processed_data)

# Salva os dados no Excel
df.to_excel(output_file, index=False)
print(f"Processamento concluído e planilha gerada: {output_file}")
