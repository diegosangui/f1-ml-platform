# 🏎️ F1 ML Platform

Plataforma de dados e machine learning para a **Fórmula 1**, construída sobre uma arquitetura moderna de dados em camadas (Medalhão). O projeto cobre todo o ciclo de vida dos dados: da coleta via API até a disponibilização para o usuário final através de um data app interativo.

---

## 📐 Arquitetura

<img width="831" height="391" alt="Image" src="https://github.com/user-attachments/assets/ccc455be-4ffe-4cf8-9293-9e4535983116"/>

---

## 🔄 Pipeline de Dados

O projeto segue a **Arquitetura Medalhão** estruturada em um bucket S3 compatível (**Supabase Storage**) e banco de dados (**Supabase DB / PostgreSQL**):

| Camada | Armazenamento | Formato | Descrição |
| :--- | :---: | :---: | :--- |
| 🛬 **Landing Zone** | Supabase Storage (S3) | `Parquet` | Dados brutos ingeridos diretamente da API, sem transformações |
| 🥉 **Bronze** | PostgreSQL (Supabase) | `Tabela SQL` | Dados brutos carregados do S3 para o banco de dados relacional |
| 🥈 **Silver** | PostgreSQL (Supabase) | `Tabela SQL` | Dados limpos, tipados e padronizados |
| 🥇 **Gold** | PostgreSQL (Supabase) | `Tabela SQL` | Dados agregados e modelados para consumo analítico e pelo modelo de ML |

### Etapas do Pipeline

1. **Coleta** — Requisições à [OpenF1 API](https://openf1.org/) para obter dados de pilotos, corridas, voltas, pit stops e telemetria.
2. **Landing Zone** — Dados salvos no formato Parquet no bucket Supabase Storage (via S3 client).
3. **Bronze (Carga)** — Leitura dos arquivos Parquet diretamente do bucket S3 e inserção no banco de dados via SQLAlchemy/Pandas.
4. **Transformação (Silver/Gold)** — Processamento e modelagem das camadas seguintes via **dbt**.
5. **ML** — Treinamento e inferência de modelo de machine learning *(em definição)*.
6. **Visualização** — Consumo dos dados através de um **Data App no Streamlit**.

---

## 🛠️ Tecnologias

| Categoria | Tecnologia |
| :--- | :--- |
| **Linguagem** | Python 3.11+ |
| **Fonte de Dados** | [OpenF1 API](https://openf1.org/) |
| **Armazenamento (Arquivos)** | Supabase Storage (S3-Compatible API) |
| **Banco de Dados (Relacional)**| PostgreSQL (Supabase) |
| **Formato de Arquivo**| Parquet |
| **Mapeamento/Conexão DB** | SQLAlchemy & Psycopg2 |
| **Transformação** | dbt |
| **Machine Learning** | A definir |
| **Data App** | Streamlit |
| **Gerenciamento** | [uv](https://github.com/astral-sh/uv) |

---

## 📦 Dependências

O projeto utiliza as seguintes dependências principais (gerenciadas via `uv`):

* **`boto3`** — SDK da AWS para interação com o bucket S3 (compatível com Supabase).
* **`pandas`** e **`fastparquet`** — Manipulação rápida de dados e salvamento no formato Parquet.
* **`sqlalchemy`** e **`psycopg2`** — Criação do engine de conexão com o banco de dados e persistência dos dados.
* **`requests`** — Consumo de dados via requisições HTTP na API do OpenF1.
* **`python-dotenv`** — Carregamento automático de variáveis de ambiente do arquivo `.env`.

---

## 🚀 Como Executar

### Pré-requisitos

* **Python 3.11+**
* [**uv**](https://github.com/astral-sh/uv) instalado localmente
* Credenciais do Supabase Storage (S3-compatible) e do Banco de Dados PostgreSQL

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
   Crie um arquivo `.env` na raiz do projeto contendo as seguintes credenciais:
   ```env
   ENDPOINT_BUCKET=https://seu-projeto-supabase.supabase.co/storage/v1/s3
   BUCKET_NAME=data-lake-f1
   REGION=us-east-1
   AWS_ACCESS_KEY_ID=sua_s3_access_key
   AWS_SECRET_ACCESS_KEY=sua_s3_secret_key
   DATABASE_URL=postgresql://usuario:senha@host:porta/banco
   ```

### Execução dos Scripts

1. **Coleta de dados da API para o Bucket S3 (Landing Zone):**
   ```bash
   uv run src/extract_api.py
   ```

2. **Consumo dos dados do S3 e carga no Banco de Dados (Camada Bronze):**
   ```bash
   uv run src/extract_bucket.py
   ```

---

## 📁 Estrutura do Projeto

```text
f1-ml-platform/
├── .vscode/
│   └── settings.json       # Configurações do VS Code (injeção automática do .env)
├── src/
│   └── coleta_dados.py     # Script de coleta de dados da OpenF1 API e upload para o S3
├── dbt/                    # Modelos de transformação (Bronze → Silver → Gold)
├── data/                   # Arquivos locais temporários (não versionados)
├── .env                    # Variáveis de ambiente (não versionado)
├── pyproject.toml          # Configuração do projeto e dependências gerenciadas pelo uv
└── README.md               # Documentação do projeto
```

---

## 📡 Fonte de Dados

Este projeto utiliza a **[OpenF1 API](https://openf1.org/)**, uma API pública e gratuita que fornece dados em tempo real e históricos da Fórmula 1, incluindo:

* 🏎️ Dados de pilotos e equipes
* 🏁 Sessões e resultados de corridas
* ⏱️ Tempos de volta e setores
* 🔧 Pit stops
* 📡 Telemetria do carro (velocidade, RPM, marcha, etc.)

---

## 🗺️ Roadmap

- [x] Conectar na API da OpenF1 (https://openf1.org/docs/#api-endpoints)
- [x] Salvar os dados em um bucket S3 (Supabase) - raw
- [x] Carregar os dados para camada bronze (PostgreSQL)
- [ ] Tratar os dados da camada bronze e carregar para camada silver
- [ ] Criar camada(s) gold com os dados agregados 
- [ ] Criar modelo(s) de ML para os dados disponibilizados
- [ ] Disponibilizar os modelos de ML em ambiente cloud
- [ ] Criar app/dash para consumo e utilização dos dados (Streamlit)

---

## 📄 Licença

Este projeto está sob a licença MIT.


