import requests as req
import pandas as pd

url = 'https://api.openf1.org/v1/drivers?session_key=latest'

response = req.get(url)
data = response.json()

df = pd.DataFrame(data)

df.to_parquet('data/pilotos.parquet', index=False)


#armazenar em arquivo parquet

#jogar para o bucket s3 - data-lake-f1