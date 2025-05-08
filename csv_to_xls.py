import pandas as pd
 
def converter_csv_para_xls(caminho_csv, caminho_xls):
    try:
        # Ler o arquivo CSV com pandas, forçando a coluna 'unidade' a ser do tipo string
        df = pd.read_csv(caminho_csv, dtype={'unidade': str})

        # Salvar o DataFrame como um arquivo XLS
        df.to_excel(caminho_xls, index=False)

        print(f"Arquivo convertido com sucesso para: {caminho_xls}")
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")

# Caminho do arquivo CSV de entrada
caminho_csv = r'C:\Users\Pc1ac\Downloads\Tratamento-de-Dados-Ser-Educacional-2-main (1)\Tratamento-de-Dados-Ser-Educacional-2\update_anuncios_json.csv'

# Caminho do arquivo XLS de saída
caminho_xls = 'anuncios_json_ser.xlsx'

# Chamar a função para converter
converter_csv_para_xls(caminho_csv, caminho_xls)