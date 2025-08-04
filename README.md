# ifood-case



## Objetivo

* Realizar a ingestão dos dados públicos de corridas de táxis de Nova York (Yellow Taxis) de **jan a mai/2023**
* Armazenar esses dados em um **Data Lake particionado por camadas (Bronze, Silver, Gold)**
* Disponibilizar os dados para análise via SQL e PySpark
* Responder a perguntas analíticas específicas

---

## Arquitetura em Camadas

* **Bronze**: Dados brutos convertidos de `.parquet`, com todos os campos disponíveis. Schema feito com base no primeiro arquivo. 
* **Silver**: Dados limpos, tipos corrigidos e adicionado coluna com tempo da viagem. 
* **Gold**: Views agregadas para consumo direto por dashboards ou analistas.

---

## Tecnologias Utilizadas

- PySpark
- Databricks Free Edition
- AWS S3
- SQL

---

## Como Executar

### Observações sobre execução no Databricks Community Edition

> A **Free Edition do Databricks utiliza clusters serverless com egress (acesso à internet) bloqueado**, o que impede o download direto dos dados da web.


Essa limitação foi verificada ao tentar rodar o código de download no script `ingestion.py`, resultando no seguinte erro: <urlopen error [Errno -3] Temporary failure in name resolution>


Isso ocorre porque o cluster **não consegue acessar URLs externas** para fazer o download dos arquivos `.parquet`.

Em um ambiente com egress habilitado seria tão simples quanto rodar diretamente o arquivo ingestion.py para obtenção dos arquivos. 

---

### Solução adotada

Como alternativa, o script `ingestion.py` foi executado **localmente**, onde:
- Os arquivos dos meses desejados (jan a mai/2023) foram baixados diretamente do site da NYC TLC
- Em seguida, os arquivos `.parquet` foram enviados para o bucket S3 (usado como *landing zone*)

---

### Como rodar localmente (para validação completa)

Se você quiser executar o processo de ingestão completo, siga os passos abaixo:

#### 1. Requisitos

- Python 3 instalado  
- AWS CLI instalado e configurado  
- Acesso a um bucket S3  

#### 2. Configurar o acesso ao S3

Execute o comando abaixo e informe suas credenciais de acesso:

`aws configure`

Exemplo de configuração (substitua com suas chaves):

`AWS Access Key ID [None]: AKIA***************`

`AWS Secret Access Key [None]: H*****************/**`

`Default region name [None]: us-east-2`

`Default output format [None]: json`

#### 3. Instalar dependências

`pip install boto3`

#### 4. Executar ingestão localmente

`python src/ingestion.py`

O script fará o download dos arquivos .parquet para o diretório local e fará o upload para o bucket S3 configurado. Após o upload dos arquivos para o S3, você pode prosseguir normalmente com os notebooks/scripts no Databricks para:

- Ingestão dos arquivos para a camada Bronze
- Transformação dos dados para a camada Silver
- Geração de métricas na camada Gold