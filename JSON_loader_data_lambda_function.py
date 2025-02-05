import os
import json
import datetime
 
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO

s3 = boto3.client('s3')
target_bucket_name = "xideraljosue"
today = datetime.today()
 
def lambda_handler(event, context):
    try:      
        # bucket_name = event['Records'][0]['s3']['bucket']['name']
        # file_key = event['Records'][0]['s3']['object']['key']
        bucket_name = "xideralcinedata"
        file_key = event["Records"][0]['s3']['object']['key']
 
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
       
        json_data = response["Body"].read().decode("utf-8")
        data = json.loads(json_data)
        df = pd.json_normalize(data)
 
        # Reemplazar nulos
        df = df.fillna(0)
 
        df['dateTime'] = pd.to_datetime(df['dateTime'])
        df['anio'] = df['dateTime'].dt.year
        df['mes'] = df['dateTime'].dt.month
        df['dia'] = df['dateTime'].dt.day
        df['hora'] = df['dateTime'].dt.hour
        df['minuto'] = df['dateTime'].dt.minute
 
        df = df.drop(columns=["dateTime"])  
 
        year_folder = str(today.year) + '/'
        month_folder = str(today.month) + '/'
        day_folder = str(today.day) + '/'
        filename = f"data_revision/{year_folder}{month_folder}{day_folder}pos_data_processed_{today.year}-{today.month}-{today.day}"
 
        target_file_content = get_target_file_content(filename)
        target_file_content = target_file_content + df.to_dict(orient='records')

        csv_dataframe = pd.DataFrame(target_file_content)
        csv_buffer = StringIO()
        csv_dataframe.to_csv(csv_buffer, index=False, header=True)

        s3.put_object(Bucket=target_bucket_name, Key=filename+".csv", Body=csv_buffer.getvalue())
        s3.put_object(Bucket=target_bucket_name, Key=filename+".json", Body=json.dumps(target_file_content, indent=4))
 
        return {
            'statusCode': 200,
            'body': "Finalizado"
        }
 
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
 
def get_target_file_content(filename: str) -> list:
    try:
        response = s3.get_object(Bucket=target_bucket_name, Key=filename)
        json_data = response["Body"].read().decode("utf-8")
        print(json_data)
        print(f"es el json data: {type(json_data)}")
        valor = json.loads(json_data)
        print(f"es el json loads: {type(valor)}")
        return valor
    except Exception as e: #Should be NoSuchKey
        print(f"No target file {filename} in {target_bucket_name}: {e}")
        return []
 