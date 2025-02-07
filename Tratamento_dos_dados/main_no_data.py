import pandas as pd
from base_no_data import load_json, process_json_data, create_dataframe

# Caminho do arquivo JSON
input_file = r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\Tratamento_dos_dados\341867950349467_insights2224_parte1.json"
output_file = "processed_data_caxangá.xlsx"

# Carrega os dados
data = load_json(input_file)

# Processa os dados
processed_data = process_json_data(data)
df = create_dataframe(processed_data)

# Salva os dados no Excel
df.to_excel(output_file, index=False)
print(f"Processamento concluído e planilha gerada: {output_file}")
