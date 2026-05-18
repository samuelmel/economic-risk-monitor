economic-risk-monitor/
│
├── 📄 README.md                          # Documentação principal
├── 📄 requirements.txt                   # Dependências Python
├── 📄 .gitignore                         # Arquivos ignorados pelo Git
├── 📄 config.py                          # Configurações centralizadas
├── 📄 main.py                            # Script principal de execução
│
├── 📂 data/                              # Dados do projeto
│   │
│   ├── 📂 raw/                           # Camada RAW (dados brutos)
│   │   └── 📂 world_bank/                # JSONs originais da API
│   │       ├── gdp_BR_2023.json
│   │       ├── inflation_US_2023.json
│   │       └── ...
│   │
│   ├── 📂 silver/                        # Camada SILVER (dados limpos)
│   │   └── 📂 world_bank/                # CSVs/Parquets limpos
│   │       ├── indicators_cleaned.csv
│   │       └── indicators_cleaned.parquet
│   │
│   ├── 📂 gold/                          # Camada GOLD (dados analíticos)
│   │   ├── country_summary.csv
│   │   ├── economic_risk_score.csv
│   │   └── aggregated_metrics.parquet
│   │
│   └── 📂 database/                      # Banco de dados SQLite
│       └── economic_risk.db
│
├── 📂 src/                               # Código fonte
│   │
│   ├── 📂 extract/                       # Camada de Extração
│   │   └── world_bank_extractor.py       # Classe para extrair da API
│   │
│   ├── 📂 transform/                     # Camada de Transformação
│   │   ├── silver_transformer.py         # Raw → Silver
│   │   └── gold_transformer.py           # Silver → Gold
│   │
│   ├── 📂 load/                          # Camada de Carga
│   │   └── database_loader.py            # Carrega dados no SQLite
│   │
│   ├── 📂 analysis/                      # Análises e Scores
│   │   └── risk_calculator.py            # Calcula score de risco
│   │
│   ├── 📂 quality/                       # Validação de Qualidade
│   │   └── data_validator.py             # Valida qualidade dos dados
│   │
│   └── 📂 utils/                         # Utilitários
│       ├── logger.py                     # Sistema de logging
│       └── database.py                   # Conexão e operações DB
│
├── 📂 sql/                               # Scripts SQL
│   ├── create_tables.sql                 # Criação de tabelas
│   ├── queries_silver.sql                # Queries camada Silver
│   └── queries_gold.sql                  # Queries camada Gold
│
├── 📂 dashboards/                        # Dashboards Streamlit
│   └── economic_dashboard.py             # Dashboard principal
│
├── 📂 tests/                             # Testes unitários
│   ├── test_extractor.py
│   ├── test_transformer.py
│   └── test_risk_calculator.py
│
└── 📂 logs/                              # Logs de execução
    └── economic_risk_20240518.log


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 DESCRIÇÃO DOS COMPONENTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────┐
│ ARQUIVOS RAIZ                                       │
└─────────────────────────────────────────────────────┘

config.py                 → Configurações (países, indicadores, URLs)
main.py                   → Orquestra todo o pipeline (Extract → Transform → Load)
requirements.txt          → Lista de dependências


┌─────────────────────────────────────────────────────┐
│ src/extract/                                        │
└─────────────────────────────────────────────────────┘

world_bank_extractor.py   → Classe WorldBankExtractor
                            • Busca dados da API
                            • Salva JSON bruto em data/raw/


┌─────────────────────────────────────────────────────┐
│ src/transform/                                      │
└─────────────────────────────────────────────────────┘

silver_transformer.py     → Classe SilverTransformer
                            • Limpa dados raw
                            • Remove nulos/duplicados
                            • Padroniza colunas
                            
gold_transformer.py       → Classe GoldTransformer
                            • Cria tabelas analíticas
                            • Agrega por país/ano
                            • Prepara dados para BI


┌─────────────────────────────────────────────────────┐
│ src/load/                                           │
└─────────────────────────────────────────────────────┘

database_loader.py        → Classe DatabaseLoader
                            • Cria tabelas SQLite
                            • Insere dados nas camadas
                            • Gerencia transações


┌─────────────────────────────────────────────────────┐
│ src/analysis/                                       │
└─────────────────────────────────────────────────────┘

risk_calculator.py        → Classe RiskCalculator
                            • Calcula score de risco
                            • Classifica (low/medium/high)
                            • Usa inflação + desemprego + PIB


┌─────────────────────────────────────────────────────┐
│ src/quality/                                        │
└─────────────────────────────────────────────────────┘

data_validator.py         → Classe DataValidator
                            • Valida schema
                            • Checa nulos/duplicados
                            • Garante consistência


┌─────────────────────────────────────────────────────┐
│ src/utils/                                          │
└─────────────────────────────────────────────────────┘

logger.py                 → Sistema de logging
database.py               → Conexão e helpers SQLite


┌─────────────────────────────────────────────────────┐
│ sql/                                                │
└─────────────────────────────────────────────────────┘

create_tables.sql         → DDL das 4 tabelas:
                            • raw_world_bank_responses
                            • silver_world_bank_indicators
                            • gold_country_summary
                            • gold_economic_risk_score


┌─────────────────────────────────────────────────────┐
│ dashboards/                                         │
└─────────────────────────────────────────────────────┘

economic_dashboard.py     → Dashboard Streamlit:
                            • Filtro por país
                            • Gráficos temporais (Plotly)
                            • Métricas econômicas
                            • Tabela analítica


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏗️ ARQUITETURA MEDALHÃO (MEDALLION ARCHITECTURE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Este projeto usa a arquitetura em camadas RAW → SILVER → GOLD:

┌─────────────────────────────────────────────────────┐
│ 🥉 RAW (Bronze) - Dados Brutos                      │
├─────────────────────────────────────────────────────┤
│ • Armazena dados exatamente como vieram da fonte    │
│ • Formato original (JSON da API)                    │
│ • Imutável - nunca é alterado                       │
│ • Permite reprocessamento completo                  │
│ • Localização: data/raw/                            │
│ • Banco: raw_world_bank_responses                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🥈 SILVER - Dados Limpos                            │
├─────────────────────────────────────────────────────┤
│ • Dados validados e limpos                          │
│ • Tipos padronizados                                │
│ • Sem nulos/duplicados                              │
│ • Formato: CSV/Parquet                              │
│ • Localização: data/silver/                         │
│ • Banco: silver_world_bank_indicators               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🥇 GOLD - Dados Analíticos                          │
├─────────────────────────────────────────────────────┤
│ • Agregado e otimizado para análise                 │
│ • Métricas de negócio calculadas                    │
│ • Pronto para dashboards e BI                       │
│ • Formato: CSV/Parquet otimizado                    │
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