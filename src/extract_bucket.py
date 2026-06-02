from connection_aws import env_s3, conn_s3
import pandas as pd
from io import BytesIO
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

response = conn_s3().list_objects(Bucket=env_s3.get('bucket_name'))

tables = [objeto['Key'] for objeto in response['Contents'] if objeto['Key'] != '.emptyFolderPlaceholder']

def ler_dados_bucket():
    for table in tables:
        df = pd.read_parquet(BytesIO(conn_s3().get_object(Bucket=env_s3.get('bucket_name'), Key=table)['Body'].read()))
        print(df.shape)

ler_dados_bucket()