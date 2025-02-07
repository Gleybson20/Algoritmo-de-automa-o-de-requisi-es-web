# Tratamento-de-Dados-Ser-Educacional-2Tratamento de Dados - Ser Educacional

📌 Visão Geral

Este projeto tem como objetivo tratar e analisar dados de campanhas publicitárias, extraídos de arquivos JSON, e gerar relatórios consolidados no formato Excel. A solução processa os dados, calcula métricas relevantes e organiza as informações de forma estruturada.

🎯 Objetivo do Projeto

O sistema permite:

Carregar arquivos JSON com informações de campanhas.

Processar os dados extraindo métricas como impressões, alcance, gastos e interações.

Gerar relatórios detalhados no formato Excel para facilitar a análise e tomada de decisão.

Mesclar múltiplos arquivos JSON em um único dataset consolidado.

🛠️ Tecnologias Utilizadas

Python (pandas, json)

SQLite (para armazenamento de dados estruturados, se necessário)

Excel (para exportação dos dados tratados)

📂 Estrutura do Projeto

Tratamento-de-Dados-Ser-Educacional-2/
│── 264383791293755_insights2224.json    # Exemplo de arquivo JSON de entrada
│── ads_databa.sql                        # Script de banco de dados
│── base_no_data.py                       # Código de processamento sem dados
│── database.py                           # Funções de manipulação de JSON
│── main.py                               # Script principal para processamento
│── mergejson.py                          # Mescla múltiplos arquivos JSON
│── processed_data.xlsx                    # Dados processados (exportação)
│── processed_data_olinda.xlsx             # Variante de exportação

🚀 Como Usar

1️⃣ Pré-requisitos

Certifique-se de ter Python instalado e as bibliotecas necessárias:

pip install pandas

2️⃣ Processar Dados

Para executar o processamento de um arquivo JSON e exportar para Excel, use:

python main.py

Isso irá carregar os dados do JSON, processá-los e gerar um arquivo processed_data.xlsx com os resultados.

3️⃣ Mesclar Arquivos JSON

Caso tenha múltiplos arquivos JSON para consolidar, use:

python mergejson.py

Isso criará um único arquivo JSON consolidado com todas as informações dos arquivos existentes.

📊 Métricas Calculadas

O sistema processa os seguintes dados:

Impressões (quantidade de exibições do anúncio)

Alcance (número de usuários únicos alcançados)

Gastos (valor investido na campanha)

Cliques (número de cliques nos anúncios)

Engajamentos (interações como curtidas e compartilhamentos)

Leads (quantidade de contatos gerados)

CTR (Click-Through Rate): Taxa de cliques sobre impressões

CPL (Custo por Lead): Custo médio por lead gerado

📌 Contribuições

Caso queira contribuir para melhorias no projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.

🚀 Este projeto foi desenvolvido para otimizar a análise de dados publicitários e facilitar a tomada de decisão com relatórios estruturados.

