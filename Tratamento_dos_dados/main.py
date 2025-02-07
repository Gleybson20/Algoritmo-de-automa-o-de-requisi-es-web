import pandas as pd
from database import load_json, process_json_data

# Caminho do arquivo JSON
input_file = "341867950349467_insights2224.json"
output_file = "processed_data_caxanga.xlsx"

# Carrega os dados
data = load_json(input_file)

# Processa os dados
processed_data = process_json_data(data)
df = pd.DataFrame(processed_data)

# Salva os dados no Excel
df.to_excel(output_file, index=False)

print(f"Processamento concluído e planilha gerada: {output_file}")
 