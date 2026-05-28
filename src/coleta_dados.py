import requests as req
import pandas as pd
from dotenv import load_dotenv
import os
import boto3
from botocore.config import Config

load_dotenv()

#variaveis de conexao no supabase S3
bucket_name = os.getenv('BUCKET_NAME')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
endpoint_url = os.getenv('ENDPOINT_BUCKET')
region_name=os.getenv('REGION')

#conexao com o supabase S3
s3_client = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

#urls de api para coleta de dados
urls = {
    'pilotos'            : 'https://api.openf1.org/v1/drivers?session_key=latest',
    'calendario_corridas': 'https://api.openf1.org/v1/sessions?year=2026&session_name=Race',
}

#funcao para coletar dados
def coletar_dados():
    for tabela, url in urls.items():
        data = req.get(url).json()
        df = pd.DataFrame(data)
        s3_client.put_object(Bucket=bucket_name, Key=f'{tabela}_2026.parquet', Body=df.to_parquet(index=False))

coletar_dados()