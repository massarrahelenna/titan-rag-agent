import streamlit as st
import boto3
import sys
import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
aws_region = os.getenv("AWS_REGION", "us-east-1")

s3_client = boto3.client('s3', region_name=aws_region)
bedrock_agent = boto3.client('bedrock-agent', region_name=aws_region)

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT / "agents") not in sys.path:
    sys.path.append(str(ROOT / "agents"))

from ask_knowledge import ask_titan_brain_stream


def upload_to_s3(file_obj, bucket, s3_path):
    """Envia o arquivo para o S3"""
    try:
        s3_client.upload_fileobj(file_obj, bucket, s3_path)
        return True
    except Exception as e:
        st.error(f"Erro no S3: {e}")
        return False

def sync_knowledge_base(kb_id, ds_id):
    """Inicia o processo de ingestão no Bedrock"""
    try:
        bedrock_agent.start_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=ds_id
        )
        return True
    except Exception as e:
        st.error(f"Erro na sincronização: {e}")
        return False

# INTERFACE UPLOAD
st.set_page_config(page_title="Titan Agent 4.6", page_icon="🤖")
st.title("🤖 Agente Titan - Claude 4.6")

with st.sidebar:
    st.header("📤 Gestão de Dados")
    uploaded_file = st.file_uploader("Upload de PDF", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Enviar e Sincronizar"):
            with st.spinner("Vetorizando documento..."):
                bucket_name = "titan-knowledge-massarra-29863"
                caminho_no_s3 = f"raw_documents/{uploaded_file.name}"
                
                # Realiza o upload
                if upload_to_s3(uploaded_file, bucket_name, caminho_no_s3):
                    st.success(f"✅ Arquivo salvo em: {caminho_no_s3}")
                    
                    ds_id = "ARSVWAGKQT" 
                    kb_id = "V9Y857FLPG"
                    
                    # Sincroniza a base de conhecimento
                    if sync_knowledge_base(kb_id, ds_id):
                        st.info("🔄 Sincronização iniciada no Bedrock!")

# INTERFACE CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte algo sobre os documentos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        def get_api_stream():
            url = f"http://backend:8000/chat?prompt={prompt}"
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            yield chunk
            except Exception as e:
                yield f"❌ Erro de conexão com a API: {e}"
                    
       
        full_response = st.write_stream(get_api_stream())
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})