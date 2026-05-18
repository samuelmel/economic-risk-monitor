# economic-risk-monitor

Projeto de ETL para dados econômicos da World Bank com arquitetura em camadas RAW → SILVER → GOLD.

## Visão Geral

Este repositório organiza coleta, limpeza, transformação e análise de indicadores econômicos usando:
- `src/extract/` para extração de dados da API
- `src/transform/` para processamento em camadas
- `src/load/` para carga em banco SQLite
- `src/analysis/` para cálculo de score de risco
- `dashboards/` para visualização com Streamlit

## Estrutura do Projeto

- `data/`
  - `raw/` — dados brutos importados da API
  - `silver/` — dados limpos e padronizados
  - `gold/` — dados analíticos preparados para BI
  - `database/` — banco SQLite utilizado pelo projeto
- `src/`
  - `extract/` — lógica de extração da API World Bank
  - `transform/` — transformações para as camadas SILVER e GOLD
  - `load/` — carregamento de dados no banco de dados
  - `analysis/` — cálculo de scores e métricas
  - `quality/` — validação de qualidade dos dados
  - `utils/` — utilitários de banco e logging
- `sql/` — scripts SQL de criação e consultas
- `dashboards/` — dashboard Streamlit
- `tests/` — testes unitários
- `logs/` — logs de execução

## Componentes Principais

### `src/extract/`
- `world_bank_extractor.py`
  - Busca dados da API do World Bank
  - Gera arquivos JSON brutos em `data/raw/`

### `src/transform/`
- `silver_transformer.py`
  - Limpa dados brutos
  - Remove nulos e duplicados
  - Padroniza colunas e formatos
- `gold_transformer.py`
  - Agrega dados em métricas analíticas
  - Prepara tabelas para BI

### `src/load/`
- `database_loader.py`
  - Cria e popula tabelas SQLite
  - Gerencia transações de carga

### `src/analysis/`
- `risk_calculator.py`
  - Calcula score de risco econômico
  - Classifica como low / medium / high
  - Utiliza inflação, desemprego e PIB

### `src/quality/`
- `data_validator.py`
  - Valida schema dos dados
  - Checa nulos e duplicados
  - Garante consistência de qualidade

### `src/utils/`
- `logger.py` — logging centralizado
- `database.py` — helpers de conexão SQLite

### `sql/`
- `create_tables.sql` — criação de tabelas
- `queries_silver.sql` — consultas da camada SILVER
- `queries_gold.sql` — consultas da camada GOLD

### `dashboards/`
- `economic_dashboard.py` — dashboard interativo para análise

## Arquitetura MEDALLION

A arquitetura adotada segue o padrão RAW → SILVER → GOLD:

### RAW
- Dados originais em formato JSON
- Mantém informação bruta sem modificações
- Localização: `data/raw/`

### SILVER
- Dados limpos e padronizados
- Remove inconsistências, nulos e duplicações
- Localização: `data/silver/`

### GOLD
- Dados agregados para análise
- Métricas calculadas e prontas para BI
- Localização: `data/gold/`

## Uso

- Rodar testes:
  ```bash
  pytest tests/
  ```
- Abrir dashboard Streamlit:
  ```bash
  streamlit run dashboards/economic_dashboard.py
  ```

## Observação

O repositório atual não inclui `requirements.txt` ou `main.py` no diretório raiz. Ajuste as dependências e os pontos de entrada conforme for necessário ao seu ambiente.
│ • Localização: data/gold/                           │
│ • Banco: gold_country_summary, gold_risk_score      │
└─────────────────────────────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 FLUXO DE DADOS (ARQUITETURA MEDALHÃO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────────────────────────────────────┐
│ CAMADA RAW (Bronze) - Dados Brutos                      │
└──────────────────────────────────────────────────────────┘

1. EXTRAÇÃO (src/extract/)
   ↓
   World Bank API → JSON bruto → data/raw/world_bank/
   
   • Mantém dados originais intocados
   • Rastreabilidade completa
   • Permite reprocessamento


┌──────────────────────────────────────────────────────────┐
│ CAMADA SILVER - Dados Limpos e Validados                │
└──────────────────────────────────────────────────────────┘

2. TRANSFORMAÇÃO SILVER (src/transform/silver_transformer.py)
   ↓
   data/raw/ → Limpeza → data/silver/ + silver_world_bank_indicators (DB)
   
   • Remove nulos e duplicados
   • Padroniza tipos de dados
   • Valida schema
   • Salva CSV/Parquet + SQLite


┌──────────────────────────────────────────────────────────┐
│ CAMADA GOLD - Dados Analíticos Agregados                │
└──────────────────────────────────────────────────────────┘

3. TRANSFORMAÇÃO GOLD (src/transform/gold_transformer.py)
   ↓
   data/silver/ → Agregação → data/gold/ + gold_country_summary (DB)
   
   • Agrega por país/ano
   • Cria métricas de negócio
   • Otimizado para análise
   • Salva CSV/Parquet + SQLite

4. ANÁLISE DE RISCO (src/analysis/risk_calculator.py)
   ↓
   data/gold/ → Cálculo de Score → gold_economic_risk_score (DB)
   
   • Calcula risk_score (0-100)
   • Classifica: low/medium/high
   • Usa inflação + desemprego + crescimento PIB

5. VISUALIZAÇÃO (dashboards/)
   ↓
   SQLite (gold_*) → Streamlit → Dashboard interativo
   
   • Lê apenas camada GOLD
   • Performance otimizada
   • Dados prontos para BI


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🗄️ ESTRUTURA DO BANCO DE DADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ raw_world_bank_responses (Camada RAW)              │
├─────────────────────────────────────────────────────┤
│ • id (PK)                                           │
│ • indicator_code                                    │
│ • country_code                                      │
│ • extraction_date                                   │
│ • raw_json (TEXT)                                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ silver_world_bank_indicators (Camada SILVER)       │
├─────────────────────────────────────────────────────┤
│ • id (PK)                                           │
│ • country_code                                      │
│ • country_name                                      │
│ • indicator_code                                    │
│ • indicator_name                                    │
│ • year                                              │
│ • value                                             │
│ • processed_at                                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ gold_country_summary (Camada GOLD)                 │
├─────────────────────────────────────────────────────┤
│ • id (PK)                                           │
│ • country_code                                      │
│ • country_name                                      │
│ • year                                              │
│ • gdp                                               │
│ • gdp_per_capita                                    │
│ • inflation                                         │
│ • unemployment                                      │
│ • population                                        │
│ • created_at                                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ gold_economic_risk_score (Camada GOLD - Analytics) │
├─────────────────────────────────────────────────────┤
│ • id (PK)                                           │
│ • country_code                                      │
│ • country_name                                      │
│ • year                                              │
│ • risk_score (0-100)                                │
│ • risk_level (low/medium/high)                      │
│ • inflation_score                                   │
│ • unemployment_score                                │
│ • gdp_growth_score                                  │
│ • calculated_at                                     │
└─────────────────────────────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 COMANDOS DE EXECUÇÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar pipeline completo
python main.py

# 3. Rodar dashboard
streamlit run dashboards/economic_dashboard.py

# 4. Rodar testes
pytest tests/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 PADRÕES DO PROJETO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ POO (Classes para cada responsabilidade)
✓ Type hints em todas as funções
✓ Logging centralizado
✓ Separação de camadas (RAW → SILVER → GOLD)
✓ Configuração centralizada (config.py)
✓ SQL separado do Python
✓ Documentação clara
✓ Pronto para produção