import requests as req
import pandas as pd
from module.connection_aws import env_s3, conn_s3
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

#urls de api para coleta de dados
urls = {
    'pilotos': 'https://api.openf1.org/v1/drivers?session_key=latest',
    'calendario_corridas': 'https://api.openf1.org/v1/sessions?year=2026&session_name=Race',
}

#funcao para coletar dados
def coletar_dados():
    for tabela, url in urls.items():
        if req.get(url).status_code == 200:
            logging.info(f"Coletando dados da tabela {tabela} na API da OpenF1")
            data = req.get(url).json()
            df = pd.DataFrame(data)
            conn_s3().put_object(
                Bucket=env_s3.get('bucket_name'),
                Key=f'{tabela}_2026.parquet',
                Body=df.to_parquet(index=False),
            )
            logging.info(
                f"Dados da tabela {tabela} armazenados no bucket {env_s3.get('bucket_name')}"
            )
        else:
            logging.warning(
                f"Erro ao coletar dados da tabela {tabela}. Status code {req.get(url).status_code}"
            )
