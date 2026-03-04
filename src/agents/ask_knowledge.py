import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

# 1. Localiza o .env na raiz do projeto titan/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

print("🚀 Iniciando o Agente Titan (Claude 4.6)...")

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def ask_titan_brain(query):
    # ID da sua Knowledge Base
    kb_id = "V9Y857FLPG" 
    
    # Perfil de Inferência Cross-Region (O que resolveu o erro anterior)
    model_id = "us.anthropic.claude-sonnet-4-6"

    orchestration_prompt = """
    Você é um orquestrador técnico. Analise a pergunta e use a base de dados.
    Histórico: $conversation_history$
    Instruções de Formato: $output_format_instructions$
    Pergunta: $query$
    """

    generation_prompt = """
    Use APENAS os trechos abaixo para responder: $search_results$
    Pergunta: $query$
    Resposta:"""

    try:
        print(f"🔍 Consultando a Knowledge Base {kb_id}...")
        response = client.retrieve_and_generate(
            input={'text': query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': model_id, 
                    'generationConfiguration': {
                        'promptTemplate': {'textPromptTemplate': generation_prompt}
                    },
                    'orchestrationConfiguration': {
                        'promptTemplate': {'textPromptTemplate': orchestration_prompt}
                    }
                }
            }
        )
        return response['output']['text']
    except Exception as e:
        return f"❌ Erro na API: {str(e)}"

# ESTE BLOCO É O QUE FAZ O SCRIPT "FALAR" NO TERMINAL
if __name__ == "__main__":
    print("✅ Script carregado com sucesso.")
    pergunta = input("\n❓ O que você deseja saber sobre os documentos? ")
    
    if pergunta.strip():
        resultado = ask_titan_brain(pergunta)
        print(f"\n🤖 Claude 4.6 responde:\n{resultado}")
    else:
        print("⚠️ Nenhuma pergunta foi digitada.")