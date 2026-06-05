from dotenv import load_dotenv
import os
import boto3
from botocore.config import Config

load_dotenv()

#variaveis de conexao no supabase S3
env_s3 = {
    'bucket_name': os.getenv('BUCKET_NAME'),
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'endpoint_url': os.getenv('ENDPOINT_BUCKET'),
    'region_name': os.getenv('REGION'),
    'database_url': os.getenv('DATABASE_URL'),
}
#conexao com o supabase S3
def conn_s3():
    s3_client = boto3.client(
        's3',
        endpoint_url=env_s3['endpoint_url'],
        aws_access_key_id=env_s3['aws_access_key_id'],
        aws_secret_access_key=env_s3['aws_secret_access_key'],
        region_name=env_s3['region_name']
    )

    return s3_client
