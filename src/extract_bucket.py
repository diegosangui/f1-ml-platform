from module.connection_aws import env_s3, conn_s3
import pandas as pd
from sqlalchemy import create_engine
from io import BytesIO
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

logging.info(f"Conectando no bucket {env_s3.get('bucket_name')}...")
response = conn_s3().list_objects(Bucket=env_s3.get('bucket_name'))

arquivos = [objeto['Key'] for objeto in response['Contents'] if objeto['Key'].endswith('.parquet')]

logging.info("Conectando no banco de dados...")
engine = create_engine(env_s3.get('database_url'))

def ler_dados_bucket():
    for arquivo in arquivos:
        df = pd.read_parquet(BytesIO(conn_s3().get_object(Bucket=env_s3.get('bucket_name'), Key=arquivo)['Body'].read()))
        df.to_sql(
            arquivo.split('.')[0],
            engine,
            if_exists='replace',
            index=False
            )
        logging.info(f"Dados da tabela {arquivo.split('.')[0]} armazenados no banco de dados")

