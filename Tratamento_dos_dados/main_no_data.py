import pandas as pd
from base_no_data import load_json, process_json_data, create_dataframe

# Caminho do arquivo JSON
input_file = r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\JSON\JSON\433757391083398_insights2224.json"
output_file = "novo_processed_data_carpipna.xlsx"

# Carrega os dados
data = load_json(input_file)

# Processa os dados
processed_data = process_json_data(data)
df = create_dataframe(processed_data)

# Salva os dados no Excel
df.to_excel(output_file, index=False)
print(f"Processamento concluído e planilha gerada: {output_file}")
