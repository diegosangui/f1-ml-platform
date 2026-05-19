import requests as req
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

url = 'https://api.openf1.org/v1/drivers?session_key=latest'

response = req.get(url)
data = response.json()

df = pd.DataFrame(data)

df.to_parquet('data/pilotos_2026.parquet', index=False)

#jogar para o bucket s3 - data-lake-f1