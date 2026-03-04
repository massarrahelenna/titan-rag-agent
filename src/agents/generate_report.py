import boto3
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Configuração de ambiente
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def ask_kb(query):
    kb_id = "V9Y857FLPG" 
    model_id = "us.anthropic.claude-sonnet-4-6" # Perfil que funcionou!

    orchestration = "Analise profundamente os papers para este relatório. Pergunta: $query$ Histórico: $conversation_history$ Formato: $output_format_instructions$"
    generation = "Você é um analista sênior. Responda de forma técnica e estruturada. Contexto: $search_results$ Pergunta: $query$ Resposta:"

    try:
        response = client.retrieve_and_generate(
            input={'text': query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': model_id,
                    'generationConfiguration': {'promptTemplate': {'textPromptTemplate': generation}},
                    'orchestrationConfiguration': {'promptTemplate': {'textPromptTemplate': orchestration}}
                }
            }
        )
        return response['output']['text'], response.get('citations', [])
    except Exception as e:
        return f"Erro: {e}", []

def gerar_relatorio():
    questoes = [
        "Quais as 3 metodologias experimentais mais comuns nestes artigos?",
        "Liste os principais benchmarks e datasets citados nos resultados.",
        "Quais são as lacunas ou 'future work' mais mencionados pelos autores?",
        "Resuma as principais métricas de performance (SOTA) alcançadas.",
        "Crie uma conclusão sintetizando o estado da arte atual baseado nestes 50 documentos."
    ]

    print(f"Gerando relatório de IA para {len(questoes)} tópicos...")
    
    with open("relatorio_tecnico.md", "w", encoding="utf-8") as f:
        f.write(f"#  Relatório de Análise Técnica - Agente Titan\n")
        f.write(f"*Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n\n")
        f.write(f"--- \n\n")

        for i, q in enumerate(questoes, 1):
            print(f"📦 Processando tópico {i}/{len(questoes)}...")
            resposta, citacoes = ask_kb(q)
            
            f.write(f"## {i}. {q}\n\n")
            f.write(f"{resposta}\n\n")
            
            if citacoes:
                f.write("### Fontes S3 Consultadas:\n")
                fontes = set()
                for c in citacoes:
                    for s in c.get('retrievedReferences', []):
                        uri = s.get('location', {}).get('s3Location', {}).get('uri', 'N/A')
                        fontes.add(uri)
                for fonte in fontes:
                    f.write(f"* {fonte}\n")
            f.write("\n---\n\n")

    print("\n✅ Relatório gerado com sucesso: relatorio_tecnico.md")

if __name__ == "__main__":
    gerar_relatorio()