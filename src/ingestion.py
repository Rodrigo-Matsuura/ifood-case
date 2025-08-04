import boto3
import urllib.request
from io import BytesIO
import time

# Configurações
aws_access_key_id = "AKIA***************"
aws_secret_access_key = "H*****************/**"
s3_bucket = "case-ifood-matsuura"
s3_landing_prefix = "newyork/landing/"

# Criação da sessão do boto3
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

s3 = session.client("s3")

# Lista dos meses
months = ["06"]
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-{}.parquet"

# Função para baixar arquivo com tentativas
def download_with_retries(url, retries=3, delay=5):
    for i in range(retries):
        try:
            response = urllib.request.urlopen(url)
            return BytesIO(response.read())
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")
            if i < retries - 1:
                print(f"Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                raise

# Loop para baixar e enviar para o S3
for month in months:
    url = base_url.format(month)
    file_name = f"yellow_tripdata_2023-{month}.parquet"
    s3_key = f"{s3_landing_prefix}{file_name}"
    
    print(f"Baixando {file_name}...")
    data = download_with_retries(url)

    print(f"Enviando {file_name} para S3...")
    s3.upload_fileobj(data, s3_bucket, s3_key)

print("Ingestão para a landing zone no S3 concluída.")

# import urllib.request

# urllib.request.urlopen("https://www.google.com").read()