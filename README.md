# 🏎️ F1 ML Platform

Plataforma de dados e machine learning para a **Fórmula 1**, construída sobre uma arquitetura moderna de dados em camadas (Medalhão). O projeto cobre todo o ciclo de vida dos dados: da coleta via API até a disponibilização para o usuário final através de um data app interativo.

---

## 📐 Arquitetura

```
┌─────────────────┐     ┌──────────────────────────────────────────┐     ┌──────────────┐
│                 │     │                  AWS S3                   │     │              │
│   OpenF1 API    │────▶│  ┌──────────┐  ┌──────────┐  ┌────────┐ │────▶│  ML Model    │
│  (Fonte de      │     │  │  Bronze  │─▶│  Silver  │─▶│  Gold  │ │     │  (TBD)       │
│   Dados)        │     │  │ Raw Data │  │ Cleaned  │  │Curated │ │     │              │
└─────────────────┘     │  └──────────┘  └──────────┘  └────────┘ │     └──────┬───────┘
                        └──────────────────────────────────────────┘            │
                                                                                ▼
                                                                        ┌──────────────┐
                                                                        │  Streamlit   │
                                                                        │  Data App    │
                                                                        └──────────────┘
```

## 🔄 Pipeline de Dados

O projeto segue a **Arquitetura Medalhão** com três camadas de dados no Amazon S3:

| Camada | Descrição |
|---|---|
| 🥉 **Bronze** | Dados brutos ingeridos diretamente da API, sem transformações |
| 🥈 **Silver** | Dados limpos, tipados e padronizados |
| 🥇 **Gold** | Dados agregados e modelados para consumo analítico e pelo modelo de ML |

### Etapas do Pipeline

1. **Coleta** — Requisições à [OpenF1 API](https://openf1.org/) para obter dados de pilotos, corridas, voltas, pit stops e telemetria
2. **Armazenamento** — Dados persistidos em formato Parquet no bucket S3 `data-lake-f1`
3. **Transformação** — Processamento e modelagem das camadas via **dbt**
4. **ML** — Treinamento e inferência de modelo de machine learning *(em definição)*
5. **Visualização** — Consumo dos dados através de um **Data App no Streamlit**

---

## 🛠️ Tecnologias

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Fonte de Dados | [OpenF1 API](https://openf1.org/) |
| Armazenamento | Amazon S3 (AWS) |
| Formato de Arquivo | Parquet |
| Transformação | dbt |
| Machine Learning | A definir |
| Data App | Streamlit |
| Gerenciador de Pacotes | [uv](https://github.com/astral-sh/uv) |

---

## 📦 Dependências

```toml
boto3           # SDK AWS para interação com o S3
fastparquet     # Leitura e escrita de arquivos Parquet
pandas          # Manipulação e análise de dados
python-dotenv   # Gerenciamento de variáveis de ambiente
requests        # Requisições HTTP para a API
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) instalado
- Credenciais AWS configuradas no arquivo `.env`

### Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone https://github.com/diegosangui/f1-ml-platform.git
   cd f1-ml-platform
   ```

2. Instale as dependências com `uv`:
   ```bash
   uv sync
   ```

3. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:
   ```env
   AWS_ACCESS_KEY_ID=sua_access_key
   AWS_SECRET_ACCESS_KEY=sua_secret_key
   AWS_DEFAULT_REGION=us-east-1
   ```

### Execução

```bash
# Coleta de dados da API e armazenamento em S3
uv run src/coleta_dados.py
```

---

## 📁 Estrutura do Projeto

```
f1-ml-platform/
├── src/
│   └── coleta_dados.py     # Script de coleta de dados da OpenF1 API
├── dbt/                    # Modelos de transformação (Bronze → Silver → Gold)
├── data/                   # Arquivos locais temporários (não versionados)
├── .env                    # Variáveis de ambiente (não versionado)
├── pyproject.toml          # Configuração do projeto e dependências
└── README.md
```

---

## 📡 Fonte de Dados

Este projeto utiliza a **[OpenF1 API](https://openf1.org/)**, uma API pública e gratuita que fornece dados em tempo real e históricos da Fórmula 1, incluindo:

- 🏎️ Dados de pilotos e equipes
- 🏁 Sessões e resultados de corridas
- ⏱️ Tempos de volta e setores
- 🔧 Pit stops
- 📡 Telemetria do carro (velocidade, RPM, marcha, etc.)

---

## 🗺️ Roadmap

- [x] Coleta de dados da OpenF1 API
- [x] Armazenamento em S3 (formato Parquet)
- [ ] Transformações dbt (camadas Bronze → Silver → Gold)
- [ ] Definição e treinamento do modelo de ML
- [ ] Data App no Streamlit
- [ ] Agendamento do pipeline (Airflow / EventBridge)

---

## 📄 Licença

Este projeto está sob a licença MIT.
