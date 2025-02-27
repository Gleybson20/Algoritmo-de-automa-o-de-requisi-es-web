import json

# 📝 Defina aqui os arquivos na ordem que deseja mesclar
files_to_merge = [
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\298926841283208_insights2224.json",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\298926841283208_insights2225.json",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\298926841283208_insights2226.json"
        
    ]

# Lista para armazenar todos os dados combinados
all_data = []

# Ler e adicionar os dados de cada arquivo na ordem especificada
for file in files_to_merge:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        all_data.extend(data)  # Adiciona os registros na lista principal

# Salvar os dados combinados em um novo arquivo JSON
output_file = "298926841283208_insights2222.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

print(f"Arquivo mesclado salvo em: {output_file}")
