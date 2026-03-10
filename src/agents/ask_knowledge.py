import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def ask_titan_brain_stream(query):
    kb_id = "V9Y857FLPG" 
    model_id = "us.anthropic.claude-sonnet-4-6"

    try:
        response = client.retrieve_and_generate_stream(
            input={'text': query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': model_id,
                }
            }
        )

        stream = response.get('stream')
        
        if stream is not None:
            for event in stream:
                if 'output' in event:
                    yield event['output']['text']
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