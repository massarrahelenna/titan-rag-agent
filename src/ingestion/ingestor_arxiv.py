import os
import boto3
import arxiv
from dotenv import load_dotenv
from pathlib import Path

# Carrega as chaves do .env
load_dotenv()

# --- CONFIGURAÇÕES ---
SEARCH_QUERIES = ["machine learning", "large language models", "agentic workflows"]
MAX_DOCS_PER_QUERY = 10  # Comece com 10 para testar o fluxo rápido
BUCKET_NAME = "titan-knowledge-massarra-29863"
KB_ID = "V9Y857FLPG"
DS_ID = "ARSVWAGKQT"

# Inicializa os clientes
s3_client = boto3.client('s3', region_name=os.getenv("AWS_REGION", "us-east-1"))
bedrock_agent = boto3.client('bedrock-agent', region_name=os.getenv("AWS_REGION", "us-east-1"))

def run_pipeline():
    client = arxiv.Client()
    Path("data").mkdir(exist_ok=True)
    
    total_enviado = 0

    for query in SEARCH_QUERIES:
        print(f"\n🔎 Buscando por: {query}")
        search = arxiv.Search(
            query=query,
            max_results=MAX_DOCS_PER_QUERY,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        for result in client.results(search):
            # Limpa o título para evitar erros de caracteres no S3
            safe_title = "".join(x for x in result.title if x.isalnum() or x in " -_").strip()
            filename = f"data/{safe_title}.pdf"
            
            print(f"📥 Baixando: {result.title}")
            result.download_pdf(dirpath="data", filename=f"{safe_title}.pdf")
            
            # Sobe para o S3
            s3_path = f"raw_documents/{safe_title}.pdf"
            try:
                s3_client.upload_file(filename, BUCKET_NAME, s3_path)
                print(f"✅ Enviado para S3: {s3_path}")
                total_enviado += 1
                
                # 🗑️ LIMPEZA: Remove o arquivo local após o upload
                os.remove(filename)
                
            except Exception as e:
                print(f"❌ Erro no upload de {safe_title}: {e}")

    # --- O GRANDE FINAL: SINCRONIZAÇÃO ---
    if total_enviado > 0:
        print("\n" + "="*30)
        print(f"🔄 Sincronizando {total_enviado} documentos no Bedrock...")
        try:
            bedrock_agent.start_ingestion_job(
                knowledgeBaseId=KB_ID, 
                dataSourceId=DS_ID
            )
            print("🚀 Sucesso! O Titan está aprendendo o conteúdo novo agora.")
        except Exception as e:
            print(f"❌ Erro ao iniciar sincronização: {e}")
    else:
        print("\n⚠️ Nenhum documento foi baixado.")

if __name__ == "__main__":
    run_pipeline()