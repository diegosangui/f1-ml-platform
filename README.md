# 🏎️ F1 ML Platform

Plataforma de dados e machine learning para a **Fórmula 1**, construída sobre uma arquitetura moderna de dados em camadas (Medalhão). O projeto cobre todo o ciclo de vida dos dados: da coleta via API até a disponibilização para o usuário final através de um data app interativo.

---

## 📐 Arquitetura

<img width="831" height="391" alt="Image" src="https://github.com/user-attachments/assets/ccc455be-4ffe-4cf8-9293-9e4535983116"/>

---

## 🔄 Pipeline de Dados

O projeto segue a **Arquitetura Medalhão** estruturada em um bucket S3 compatível (**Supabase Storage**) e banco de dados relacional (**PostgreSQL / Supabase DB**):

| Camada | Armazenamento | Formato | Descrição |
| :--- | :---: | :---: | :--- |
| 🛬 **Landing Zone** | Supabase Storage (S3) | `Parquet` | Dados brutos ingeridos diretamente da API, sem transformações |
| 🥉 **Bronze** | PostgreSQL (Supabase) | `Tabela SQL` | Dados brutos carregados do S3 para o banco de dados (via dbt) |
| 🥈 **Silver** | PostgreSQL (Supabase) | `Tabela SQL` | Dados limpos, tipados e padronizados (via dbt) |
| 🥇 **Gold** | PostgreSQL (Supabase) | `Tabela SQL` | Dados agregados e modelados para consumo analítico (via dbt) |

### Etapas do Pipeline

1. **Coleta** — Requisições à [OpenF1 API](https://openf1.org/) para obter dados de pilotos, sessões e resultados de corridas.
2. **Landing Zone** — Dados salvos no formato Parquet no bucket Supabase Storage (via S3 client com `boto3`). Pilotos e sessões são salvos como arquivos únicos; resultados de sessão são particionados por timestamp em `results/`.
3. **Bronze (Carga)** — Leitura dos arquivos Parquet diretamente do bucket S3 e inserção no banco de dados via SQLAlchemy/Pandas.
4. **Transformação Silver** — Limpeza, tipagem e padronização dos dados via **dbt** (modelos: `silver_pilotos`, `silver_sessoes`, `silver_resultadosessoes`).
5. **Camada Gold** — Modelagem analítica com dados agregados via **dbt** (modelos: `pilotos_2026`, `classificacao_2026`, `calendario_2026`).
6. **ML** — Treinamento e inferência de modelo de machine learning *(em desenvolvimento)*.
7. **Visualização** — Consumo dos dados através de um **Data App no Streamlit** *(em desenvolvimento)*.

---

## 🗂️ Modelos dbt

Os modelos dbt estão organizados nas três camadas da arquitetura Medalhão, dentro do diretório `dbt/models/`. Cada camada é materializada como `table` em seu próprio schema no PostgreSQL, configurados via `dbt_project.yml`.

### 🥉 Bronze
| Modelo | Schema | Tags | Descrição |
| :--- | :---: | :---: | :--- |
| `bronze_pilotos` | `bronze` | `bronze`, `raw_data` | Dados brutos dos pilotos carregados da fonte raw |
| `bronze_sessoes` | `bronze` | `bronze`, `raw_data` | Dados brutos das sessões/calendário |
| `bronze_resultadosessoes` | `bronze` | `bronze`, `raw_data` | Dados brutos dos resultados de cada sessão |

### 🥈 Silver
| Modelo | Schema | Tags | Descrição |
| :--- | :---: | :---: | :--- |
| `silver_pilotos` | `silver` | `silver`, `cleaned_data` | Pilotos com colunas tipadas e renomeadas para português |
| `silver_sessoes` | `silver` | `silver`, `cleaned_data` | Sessões com colunas tipadas, renomeadas e filtradas |
| `silver_resultadosessoes` | `silver` | `silver`, `cleaned_data` | Resultados de sessões limpos e tipados |

### 🥇 Gold
| Modelo | Schema | Tags | Descrição |
| :--- | :---: | :---: | :--- |
| `pilotos_2026` | `gold` | `gold`, `analytics_data` | Pilotos ativos na temporada 2026 (Corridas e Sprints) |
| `classificacao_2026` | `gold` | `gold`, `analytics_data` | Classificação dos pilotos na temporada 2026 com pontuação, vitórias e posição |
| `calendario_2026` | `gold` | `gold`, `analytics_data` | Calendário de provas da temporada 2026 |

---

## 🛠️ Tecnologias

| Categoria | Tecnologia |
| :--- | :--- |
| **Linguagem** | Python 3.11+ |
| **Gerenciamento de Pacotes** | [uv](https://github.com/astral-sh/uv) |
| **Fonte de Dados** | [OpenF1 API](https://openf1.org/) |
| **Armazenamento (Arquivos)** | Supabase Storage (S3-Compatible API) |
| **Banco de Dados** | PostgreSQL (Supabase DB) |
| **Formato de Arquivo** | Parquet |
| **SDK S3** | boto3 + botocore |
| **Mapeamento/Conexão DB** | SQLAlchemy & Psycopg2 |
| **Serialização Parquet** | PyArrow |
| **Transformação** | dbt-core / dbt-postgres |
| **Automação / CI** | GitHub Actions |
| **Variáveis de Ambiente** | python-dotenv |
| **Logging** | Python `logging` (stdlib) |
| **Machine Learning** | *(a definir)* |
| **Data App** | Streamlit *(em desenvolvimento)* |

---

## 📦 Dependências

O projeto utiliza as seguintes dependências principais (gerenciadas via `uv`):

* **`boto3`** — SDK da AWS para interação com o bucket S3 (compatível com Supabase).
* **`pandas`** — Manipulação e estruturação de dados em DataFrames.
* **`pyarrow`** — Engine de serialização/desserialização de arquivos Parquet.
* **`requests`** — Consumo de dados via requisições HTTP na API do OpenF1.
* **`python-dotenv`** — Carregamento automático de variáveis de ambiente do arquivo `.env`.
* **`sqlalchemy`** e **`psycopg2`** — Criação do engine de conexão com o banco de dados.
* **`dbt-core`** e **`dbt-postgres`** — Ferramentas de transformação de dados e modelagem.

---

## 🚀 Como Executar

### Pré-requisitos

* **Python 3.11+**
* [**uv**](https://github.com/astral-sh/uv) instalado localmente
* Credenciais do Supabase (Storage e DB)

### Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/diegosangui/f1-ml-platform.git
   cd f1-ml-platform
   ```

2. **Instale as dependências com `uv`:**
   ```bash
   uv sync
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as seguintes credenciais:
   ```env
   ENDPOINT_BUCKET=https://seu-projeto-supabase.supabase.co/storage/v1/s3
   BUCKET_NAME=data-lake-f1
   REGION=us-east-1
   AWS_ACCESS_KEY_ID=sua_s3_access_key
   AWS_SECRET_ACCESS_KEY=sua_s3_secret_key
   DATABASE_URL=postgresql://usuario:senha@host:porta/banco
   ```

### Execução dos Scripts

1. **Coleta de dados da API para o S3 (Landing Zone):**
   ```bash
   uv run src/extract_api.py
   ```
   > Coleta dados de pilotos, sessões e resultados da [OpenF1 API](https://openf1.org/) e os salva no formato Parquet no bucket S3 do Supabase. Resultados de sessão são particionados por timestamp em `results/`.

2. **Carga dos dados do S3 para o Banco de Dados (Bronze — tabelas raw):**
   ```bash
   uv run src/extract_bucket.py
   ```
   > Lê todos os arquivos `.parquet` do bucket e os carrega nas tabelas brutas do PostgreSQL. Tabelas de pilotos e sessões são substituídas (`replace`); resultados de sessão são acumulados (`append`).

3. **Transformação com dbt (Bronze → Silver → Gold):**
   ```bash
   cd dbt
   dbt run
   ```
   > Executa todos os modelos dbt, populando as camadas Bronze, Silver e Gold no banco de dados.

   Para executar uma camada específica:
   ```bash
   dbt run --select bronze   # Apenas camada Bronze
   dbt run --select silver   # Apenas camada Silver
   dbt run --select gold     # Apenas camada Gold
   ```

   Para executar um modelo específico com todas as suas dependências:
   ```bash
   dbt run --select +classificacao_2026   # Classificação e dependências upstream
   ```

---

## ⚙️ Automação — GitHub Actions

O pipeline de extração é executado automaticamente toda **segunda-feira às 06:00 UTC** via [GitHub Actions](.github/workflows/extract.yml), sem necessidade de intervenção manual. Também é possível disparar a execução manualmente pela interface do GitHub (`workflow_dispatch`).

### Fluxo de execução

```
┌────────────────────────────────┐
│        Trigger (schedule)      │
│  toda segunda-feira às 06:00 UTC│
│  + execução manual (dispatch)  │
└────────────────┬───────────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │  Job: extract-api      │
    │  OpenF1 API → S3       │
    │  (extract_api.py)      │
    └────────────┬───────────┘
                 │  needs: extract-api
                 ▼
    ┌────────────────────────┐
    │  Job: extract-bucket   │
    │  S3 → PostgreSQL       │
    │  (extract_bucket.py)   │
    └────────────┬───────────┘
                 │  needs: extract-bucket
                 ▼
    ┌────────────────────────┐
    │  Job: dbt-run          │
    │  Bronze → Silver → Gold│
    │  (dbt run + dbt test)  │
    └────────────────────────┘
```

### Secrets necessários

Configure em **Settings → Secrets and variables → Actions** do repositório:

#### Jobs `extract-api` e `extract-bucket`

| Secret | Descrição |
| :--- | :--- |
| `BUCKET_NAME` | Nome do bucket no Supabase Storage |
| `AWS_ACCESS_KEY_ID` | Access key do S3 (Supabase) |
| `AWS_SECRET_ACCESS_KEY` | Secret key do S3 (Supabase) |
| `ENDPOINT_BUCKET` | URL do endpoint S3 do Supabase |
| `REGION` | Região do bucket (ex: `us-east-1`) |
| `DATABASE_URL` | Connection string do PostgreSQL |

#### Job `dbt-run`

| Secret | Descrição |
| :--- | :--- |
| `DB_HOST` | Host do banco de dados PostgreSQL |
| `DB_PORT` | Porta do banco de dados (ex: `5432`) |
| `DB_USER` | Usuário do banco de dados |
| `DB_PASSWORD` | Senha do banco de dados |
| `DB_NAME` | Nome do banco de dados |

> Os valores desses secrets correspondem às mesmas variáveis do arquivo `.env` local.

---

## 📁 Estrutura do Projeto

```text
f1-ml-platform/
├── .github/
│   └── workflows/
│       └── extract.yml         # Workflow de extração automática semanal (GitHub Actions)
├── .vscode/
│   └── settings.json           # Configurações do VS Code (injeção automática do .env)
├── dbt/
│   ├── models/
│   │   ├── _sources.yml        # Definição das fontes de dados (tabelas raw no PostgreSQL)
│   │   ├── bronze/
│   │   │   ├── bronze_pilotos.sql
│   │   │   ├── bronze_sessoes.sql
│   │   │   └── bronze_resultadosessoes.sql
│   │   ├── silver/
│   │   │   ├── silver_pilotos.sql
│   │   │   ├── silver_sessoes.sql
│   │   │   └── silver_resultadosessoes.sql
│   │   └── gold/
│   │       ├── pilotos_2026.sql
│   │       ├── classificacao_2026.sql
│   │       └── calendario_2026.sql
│   └── dbt_project.yml         # Configuração do projeto dbt (perfil, schemas, tags)
├── src/
│   ├── module/
│   │   └── connection_aws.py   # Módulo de conexões (S3 client e PostgreSQL engine)
│   ├── extract_api.py          # Extração de dados da OpenF1 API → Landing Zone (S3)
│   └── extract_bucket.py       # Carga dos dados S3 (Landing Zone) → PostgreSQL (Bronze raw)
├── logs/                       # Logs de execução (não versionados)
├── .env                        # Variáveis de ambiente (não versionado)
├── pyproject.toml              # Configuração do projeto e dependências (uv)
└── README.md                   # Documentação do projeto
```

---

## 📡 Fonte de Dados

Este projeto utiliza a **[OpenF1 API](https://openf1.org/)**, uma API pública e gratuita que fornece dados em tempo real e históricos da Fórmula 1, incluindo:

* 🏎️ Dados de pilotos e equipes
* 🏁 Sessões e resultados de corridas
* ⏱️ Tempos de volta e setores
* 🔧 Pit stops
* 📡 Telemetria do carro (velocidade, RPM, marcha, etc.)

### Endpoints Utilizados

| Endpoint | Descrição |
| :--- | :--- |
| `/v1/drivers` | Dados e informações dos pilotos |
| `/v1/sessions` | Sessões (treinos, classificação, corridas, sprints) |
| `/v1/session_result` | Resultados de cada sessão (posição, pontos) |

---

## 🗺️ Roadmap

- [x] Conectar na API da OpenF1
- [x] Salvar os dados em um bucket S3 (Supabase)
- [x] Carregar os dados para camada bronze (PostgreSQL)
- [x] Tratar os dados da camada bronze e carregar para camada silver (via dbt)
- [x] Criar camada(s) gold com os dados agregados (via dbt)
- [x] Automatizar o pipeline de extração com GitHub Actions (schedule semanal)
- [x] Automatizar a execução do dbt com GitHub Actions (dbt run + dbt test)
- [ ] Criar validação de erros e qualidade de dados
- [ ] Criar modelo(s) de ML para os dados disponibilizados
- [ ] Disponibilizar os modelos de ML em ambiente cloud
- [ ] Criar app/dash para consumo e utilização dos dados (Streamlit)


---

## 📄 Licença

Este projeto está sob a licença MIT.
