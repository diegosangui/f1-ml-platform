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

#conexao com o supabase S3
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('ENDPOINT_BUCKET'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION')
)

#url de api para coleta de dados
url = 'https://api.openf1.org/v1/drivers?session_key=latest'

data = req.get(url).json()
df = pd.DataFrame(data)

#envio de arquivo parquet para supabase s3
s3_client.put_object(Bucket=os.getenv('BUCKET_NAME'), Key='pilotos_2026.parquet', Body=df.to_parquet(index=False))
