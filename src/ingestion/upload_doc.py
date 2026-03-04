import boto3
import os
from pathlib import Path
from dotenv import load_dotenv


# __file__ é o caminho deste script. .parent é ingestion/, .parent.parent é src/, .parent.parent.parent é titan/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

s3 = boto3.client('s3')
# Define o caminho para a pasta de dados na raiz
DATA_PATH = BASE_DIR / "data" / "raw_pdfs"

def upload_to_s3():
    bucket = os.getenv('S3_BUCKET_NAME')
    
    if not bucket:
        print("❌ Erro: S3_BUCKET_NAME não encontrado no .env")
        return

    print(f"📂 Procurando PDFs em: {DATA_PATH}")
    
    # Verifica se a pasta realmente existe
    if not DATA_PATH.exists():
        print(f"Erro: A pasta {DATA_PATH} não existe!")
        return

    files = list(DATA_PATH.glob("*.pdf"))
    
    if len(files) == 0:
        print("Nenhum PDF encontrado. Verifique se os arquivos estão na pasta data/raw_pdfs/")
        return

    print(f"Encontrados {len(files)} PDFs. Iniciando upload para o Claude 4.6 processar...")

    for file_path in files:
        s3_key = f"raw_documents/{file_path.name}"
        try:
            print(f"⬆Subindo {file_path.name}...")
            s3.upload_file(str(file_path), bucket, s3_key)
        except Exception as e:
            print(f"Erro ao subir {file_path.name}: {e}")

    print(f"Sucesso! Seus PDFs estão em s3://{bucket}/raw_documents/  :)")

if __name__ == "__main__":
    upload_to_s3()