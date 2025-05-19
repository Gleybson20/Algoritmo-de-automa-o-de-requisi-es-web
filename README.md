# 📊 Tratamento de Dados - Ser Educacional   

## 📌 Visão Geral
Este projeto tem como objetivo **extrair, tratar e analisar dados de campanhas publicitárias** do **Meta Ads API**, processá-los e gerar **um Dashboard para visualização e análise das métricas calculadas**.  

A solução permite automatizar o tratamento dos dados, calcular métricas de desempenho e consolidar informações de forma estruturada, facilitando a análise e a tomada de decisões.  

---

## 🎯 Objetivos do Projeto  

✔ **Carregar arquivos JSON** contendo informações de campanhas publicitárias.  
✔ **Processar os dados**, extraindo métricas como **impressões, alcance, gastos e interações**.  
✔ **Gerar relatórios** detalhados no formato **Excel**.  
✔ **Realizar requisições automáticas** à API do Meta Ads.  
✔ **Mesclar múltiplos arquivos JSON** em um único dataset consolidado.
✔ **Exportar diariamente os dados para um DashBoard**.

---

## 🛠️ Tecnologias Utilizadas  

| Tecnologia | Descrição |
|------------|--------------------------------|
| **Python** | Linguagem principal do projeto |
| **pandas** | Processamento e análise de dados |
| **requests** | Conexão com a API do Meta Ads |
| **json** | Manipulação de arquivos JSON |
| **SQLite** | Armazenamento de dados estruturados (se necessário) |
| **Excel (.xlsx)** | Exportação dos dados tratados |
| **GitHub** | Automação de requisições diárias |
| **Supabase** | Armazenamento dos dados | 
| **Power BI** | Visualzação das métricas | 

---

# 📁 Estrutura do Projeto - Tratamento de Dados

```

📂 Algoritmo de Automação de requisições
├── 📂 Tratamento dos dados
│   ├── anuncios_json_ser.xlsx
│   ├── base_no_data.py
│   ├── main_no_data.py
│   ├── update_anuncios_json.csv
│
├── 📂 scripts
│   ├── 📜 algoritmo_de_busca.py
│   ├── 📜 coletor_automático.py
│   ├── 📜 script\_caso\_de\_erro.py
│   ├── 📜 mover_arquivos.py
│   ├── 📜 script\_primeiro\_request.py
│   ├── 📜 script\_todo\_dia.py
│   ├── 📜 scriptunico.py
│
├── 📂 Banco de Dados
│   ├── create_database.py
│   ├──create_tables.py
│   ├──db_conexao.py
│   ├──importar_JSON.py
│
├── 📂 venv
│
└── 📄 README.md

````

---

## 📊 **Fluxo do Projeto Atualizado**  
Abaixo está um diagrama ilustrando o funcionamento atualizado do projeto:  

```mermaid
graph TD;
    A[Requisição de Dados da API Meta Ads] -->|JSON| B[Processamento dos Dados]
    B -->|Tratamento dos dados no PostgreSQL| C[Exportação dos dados para o Supabase]
    C -->|Atualização para o DashBoard| D[Usuário Final]
````

---

# 📈 Métricas Monitoradas

| **Métrica**                        | **Descrição**                                                                      |
| ---------------------------------- | ---------------------------------------------------------------------------------- |
| 💰 **Custo por Resultado**         | Avalia o custo médio investido para cada resultado alcançado.                      |
| 📊 **Investimento x Resultado**    | Relação entre o valor investido e os resultados obtidos nas campanhas.             |
| 🏆 **Ranking por Unidades**        | Classificação das unidades (campanhas, conjuntos ou anúncios) conforme desempenho. |
| 📈 **Resultado ao longo do tempo** | Evolução dos resultados nas campanhas analisadas por períodos.                     |

---

# 🚀 Uso do Projeto
# 📌 Pré-requisitos
Antes de começar, instale as bibliotecas necessárias:

```
pip install pandas requests openpyxl psycopg2-binary sqlalchemy
```
Obs: psycopg2-binary e sqlalchemy são necessários para manipulação do PostgreSQL.

# 🛠️ Passo a passo para execução

## 1️⃣ Coleta automática dos dados da API Meta Ads
Execute o script coletor_automatico.py para baixar os dados de todas as unidades em JSON, conforme o período configurado:

```
python Tratamento_dos_dados/coletor_automatico.py
```

O que faz:

Requisita e salva arquivos JSON com dados das 59 unidades.


## 2️⃣ Criação e configuração do banco PostgreSQL
Na pasta Banco_de_Dados, execute os scripts na ordem para:

Criar a base de dados e tabelas necessárias;

Definir colunas e tipos;

Importar os arquivos JSON para o PostgreSQL.

Consulte os cabeçalhos dos scripts para mais detalhes.

## 3️⃣ Exportação da base para CSV
Após importar os dados no PostgreSQL, utilize o script indicado para exportar a base em CSV para análise.


## 4️⃣ Análise e geração dos relatórios Excel
Por fim, execute o script main.py para processar os dados CSV e gerar os relatórios Excel consolidados:

```
python Tratamento_dos_dados/main.py
```

# 🛠️ Possíveis Erros e Soluções:


## ❌ Erro: FileNotFoundError
Causa: Arquivo JSON ou CSV não encontrado.
✅ Solução: Execute os scripts na ordem correta para garantir geração e localização dos arquivos.



## ❌ Erro: Problemas na conexão com PostgreSQL
Causa: Configuração incorreta ou serviço não ativo.
✅ Solução: Verifique credenciais no arquivo de configuração e se o PostgreSQL está rodando.



## ❌ Erro: API retornando dados vazios
Causa: Parâmetros de data incorretos no coletor.
✅ Solução: Ajuste o período no coletor_automatico.py para datas válidas.
