import requests as req
from datetime import datetime as dt
import pandas as pd
import json
from module.connection_aws import env_s3, conn_s3
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

#urls de api para coleta de dados
urls = {
    'pilotos': 'https://api.openf1.org/v1/drivers',
    'sessoes': 'https://api.openf1.org/v1/sessions',
    'resultados_sessoes': 'https://api.openf1.org/v1/session_result',
}

data_atual = dt.now().strftime('%Y%m%d%H%M%S')

#funcao para coletar dados
def coletar_dados():
    for tabela, url in urls.items():
        response = req.get(url)
        if response.status_code == 200:
            logging.info(f"Coletando dados de {tabela} na API da OpenF1")
            data = response.json()
            df = pd.DataFrame(data)
            #tratamento de listas
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, list)).any():
                    df[col] = df[col].apply(
                        lambda x: json.dumps(x) if isinstance(x, list) else None if pd.isna(x) else str(x)
                    )
            if tabela == 'resultados_sessoes':
                 conn_s3().put_object(
                    Bucket=env_s3['bucket_name'],
                    Key=f'results/{tabela}{data_atual}.parquet',
                    Body=df.to_parquet(engine="pyarrow", index=False),
                )             
            else:  
                conn_s3().put_object(
                    Bucket=env_s3['bucket_name'],
                    Key=f'{tabela}.parquet',
                    Body=df.to_parquet(engine="pyarrow", index=False),
                )
            logging.info(
                f"Dados da tabela {tabela} armazenados no bucket {env_s3['bucket_name']}"
            )
        else:
            logging.warning(
                f"Erro ao coletar dados de {tabela}. Status code {response.status_code}: {response.text}"
            )
coletar_dados()