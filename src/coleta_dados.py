import requests as req
import pandas as pd
from dotenv import load_dotenv
import io
import os
import boto3
from botocore.config import Config
#import pyarrow as pa
#import pyarrow.parquet as pq

load_dotenv()

bucket_name = os.getenv('BUCKET_NAME')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

url = 'https://api.openf1.org/v1/drivers?session_key=latest'

response = req.get(url)
data = response.json()

df = pd.DataFrame(data)

df.to_parquet('data/pilotos_2026.parquet', index=False)

# #jogar para o bucket s3 - data-lake-f1


# #função jogar dados para o bucket s3
# def jogar_dados_s3(df, bucket_name, key):
#     s3 = boto3.client('s3', 
#                       aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#                       aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
#     s3.put_object(Bucket=bucket_name, Key=key, Body=df.to_parquet(index=False))


s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('ENDPOINT_BUCKET'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('REGION')
)

s3_client.put_object(Bucket=os.getenv('BUCKET_NAME'), Key='pilotos_2026.parquet', Body=df.to_parquet(index=False))
