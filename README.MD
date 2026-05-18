# Teste Técnico - Assistente de Dados / Analista de Dados Júnior

Projeto desenvolvido para o teste técnico da vaga de **Assistente de Dados / Analista de Dados Júnior**.

## Visão Geral

Este repositório implementa um pipeline de dados em três camadas:

- **RAW**: dados brutos extraídos da API
- **SILVER**: dados tratados e padronizados
- **GOLD**: dados agregados prontos para análise

A orquestração é feita com **Apache Airflow**, a extração em **Python** e as transformações em **SQL**.

## Fonte de Dados

Os dados são extraídos da API pública JSONPlaceholder:

- Usuários: `https://jsonplaceholder.typicode.com/users`
- Posts: `https://jsonplaceholder.typicode.com/posts`

A API não requer autenticação.

## Estrutura do Projeto

- `src/extract_api.py` — funções de extração e transformação inicial em pandas
- `dags/` — definição das DAGs do Airflow
- `scripts/create_raw_tables.sql` — criação das tabelas RAW
- `scripts/create_silver_tables.sql` — criação das tabelas SILVER
- `scripts/create_gold_tables.sql` — criação das tabelas GOLD
- `scripts/transformations/` — scripts SQL de transformação entre camadas

## Camadas do Pipeline

### RAW

A camada RAW recebe os dados brutos extraídos da API.

Tabelas:

- `raw_usuarios`
- `raw_posts`

A extração é feita por:

- `src/extract_api.py`

### SILVER

A camada SILVER contém dados limpos e padronizados.

Tabelas:

- `silver_usuarios`
- `silver_posts`

Transformações SQL aplicadas:

- rename de campos
- extração de cidade e empresa
- construção de domínio de email
- remoção de quebras de linha em posts
- truncamento de texto de post em 500 caracteres
- cálculo de quantidade de palavras no título

### GOLD

A camada GOLD contém métricas agregadas:

- `gold_metricas_usuario`

Métricas entregues:

- total de posts por usuário
- média de palavras nos títulos
- primeiro post de cada usuário
- informações de cidade e empresa do usuário

## Dependências

- Python 3.9+
- pandas
- requests
- sqlalchemy
- psycopg2-binary
- apache-airflow-providers-postgres

Instale os requisitos com:

```bash
pip install -r requirements.txt
```

## Configuração do Banco de Dados

O projeto usa PostgreSQL.

Antes de executar as DAGs, crie as tabelas necessárias com os scripts:

```bash
psql < scripts/create_raw_tables.sql
psql < scripts/create_silver_tables.sql
psql < scripts/create_gold_tables.sql
```

> Ajuste o comando acima conforme a sua conexão com o PostgreSQL.

## Configuração do Airflow

As DAGs usam a conexão do Airflow:

- `postgres_default`

Certifique-se de que essa conexão aponte para seu banco PostgreSQL.

### DAGs disponíveis

| DAG | Agendamento | Descrição |
| --- | --- | --- |
| `etl_raw_extract` | `06:00` | Extrai dados da API e carrega a camada RAW |
| `etl_silver_transform` | `06:30` | Transforma dados da RAW para SILVER |
| `etl_gold_aggregate` | `07:00` | Agrega dados da SILVER para GOLD |

## Execução do Pipeline

Ordem de execução:

1. `etl_raw_extract`
2. `etl_silver_transform`
3. `etl_gold_aggregate`

### 1. Criar tabelas

Execute:

```bash
psql < scripts/create_raw_tables.sql
psql < scripts/create_silver_tables.sql
psql < scripts/create_gold_tables.sql
```

### 2. Executar a DAG RAW

DAG: `etl_raw_extract`

Carrega:

- `raw_usuarios`
- `raw_posts`

### 3. Executar a DAG SILVER

DAG: `etl_silver_transform`

Executa:

- `scripts/transformations/raw_to_silver_usuarios.sql`
- `scripts/transformations/raw_to_silver_posts.sql`

### 4. Executar a DAG GOLD

DAG: `etl_gold_aggregate`

Executa:

- `scripts/transformations/silver_to_gold_metricas.sql`

## Extração em Python

O arquivo `src/extract_api.py` contém as funções:

- `fetch_usuarios()`
- `fetch_posts()`
- `flatten_usuario()`
- `extract_usuarios()`
- `extract_posts()`

Essas funções:

- fazem chamadas HTTP com `requests`
- tratam erros de conexão com `try/except`
- achatam campos aninhados do JSON de usuário
- constroem `DataFrame`s com `pandas`
- adicionam a coluna `dl_load_timestamp`

## Transformações SQL

### RAW → SILVER (usuários)

Arquivo:

- `scripts/transformations/raw_to_silver_usuarios.sql`

### RAW → SILVER (posts)

Arquivo:

- `scripts/transformations/raw_to_silver_posts.sql`

### SILVER → GOLD

Arquivo:

- `scripts/transformations/silver_to_gold_metricas.sql`


Autor Samuel Mendes