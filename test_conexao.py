import boto3
from dotenv import load_dotenv
import os

# Força o carregamento do .env
load_dotenv()

def test_aws():
    # Verifica se as variáveis foram carregadas
    if not os.getenv('AWS_ACCESS_KEY_ID'):
        print("❌ Erro: Arquivo .env não encontrado ou variáveis vazias!")
        return

    try:
        # Este comando identifica quem está logado
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ Conectado como o usuário: {identity['Arn']}")

        # Agora tenta listar os buckets
        s3 = boto3.client('s3')
        s3.list_buckets()
        print("✅ Permissão de S3: OK!")
        
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_aws()