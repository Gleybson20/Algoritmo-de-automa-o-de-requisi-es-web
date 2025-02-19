import json

# 📝 Defina aqui os arquivos na ordem que deseja mesclar
files_to_merge = [
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\1758023371040322_insights2224_parte1.json",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\1758023371040322_insights2224_parte2.json",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\1758023371040322_insights2224_parte3.json",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\1758023371040322_insights2224_parte4.json",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\1758023371040322_insights2224_parte5.json",
    r"C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\1758023371040322_insights2224_parte6.json"
     ]

# Lista para armazenar todos os dados combinados
all_data = []

# Ler e adicionar os dados de cada arquivo na ordem especificada
for file in files_to_merge:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        all_data.extend(data)  # Adiciona os registros na lista principal

# Salvar os dados combinados em um novo arquivo JSON
output_file = "1758023371040322_insights2224.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

print(f"Arquivo mesclado salvo em: {output_file}")
