import boto3
import os
from botocore.config import Config
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))

def get_presigned_url(s3_uri):
    """Gera o link temporário para o PDF"""
    try:
        parts = s3_uri.replace("s3://", "").split("/")
        bucket = parts[0]
        key = "/".join(parts[1:])
        return s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3600
        )
    except:
        return None
def ask_titan_brain_stream(query):
    kb_id = "V9Y857FLPG" 
    model_id = "us.anthropic.claude-sonnet-4-6"
   
    system_prompt = "Você é um assistente técnico."
    if any(x in query.lower() for x in ["tabela", "compare", "comparativo"]):
        system_prompt = (
            "Você é um Analista de Dados Científicos. Sua tarefa é extrair fatos dos documentos "
            "e organizá-los em uma TABELA MARKDOWN. Use colunas como 'Paper', 'Metodologia' e 'Resultado'."
        )
    try:
        response = client.retrieve_and_generate_stream(
            input={'text': query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': model_id,
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': f"{system_prompt}\n\nResponda à pergunta usando o contexto: $search_results$\n\nPergunta: $query$"
                        }
                    }
                }
            }
        )

        stream = response.get('stream')
        sources = {}
        
        if stream is not None:
            for event in stream:
                if 'output' in event:
                    yield event['output']['text']
                if 'citation' in event:
                    citations = event['citation'].get('generatedResponsePart', {}).get('retrievedReferences', [])
                    for ref in citations:
                        uri = ref['location']['s3Location']['uri']
                        file_name = uri.split('/')[-1]
                        if file_name not in sources:
                            sources[file_name] = get_presigned_url(uri)
            if sources:
                yield "\n\n--SOURCES--\n" + "\n".join([f"{name}|{url}" for name, url in sources.items()])
        else:
            yield "⚠️ A IA não encontrou resposta. Verifique se o documento já terminou de sincronizar no console da AWS."

    except Exception as e:
        yield f"❌ Erro na orquestração: {str(e)}"

if __name__ == "__main__":
    print("🚀 Testando Agente Titan em modo Streaming...")
    pergunta = input("\nO que você deseja saber? ")
    
    if pergunta.strip():
        print("\nO agente responde: ", end="", flush=True)
        for pedaco in ask_titan_brain_stream(pergunta):
            print(pedaco, end="", flush=True)
        print("\n")
    else:
        print("Nenhuma pergunta digitada.")