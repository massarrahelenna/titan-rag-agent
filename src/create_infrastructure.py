import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def setup_storage():
    s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION'))
    # Criando um nome único baseado no seu usuário
    bucket_name = f"titan-knowledge-massarra-{os.getpid()}"
    
    try:
        # Criação do Bucket na região us-east-1
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' criado com sucesso!")
        
        # Salva o nome do bucket no seu .env automaticamente para os próximos scripts
        with open(".env", "a") as f:
            f.write(f"\nS3_BUCKET_NAME={bucket_name}")
        
        return bucket_name
    except Exception as e:
        print(f"❌ Erro ao criar bucket: {e}")

if __name__ == "__main__":
    setup_storage()