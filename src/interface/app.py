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
        # 1. Criamos um container vazio para o texto "digitando"
        container = st.empty()
        full_content = ""
        actual_text = ""
        sources_raw = ""

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

        for chunk in get_api_stream():
            full_content += chunk
            
            if "--SOURCES--" in full_content:
                parts = full_content.split("--SOURCES--")
                actual_text = parts[0]
                sources_raw = parts[1] if len(parts) > 1 else ""
                container.markdown(actual_text + "▌")
            else:
                actual_text = full_content
                container.markdown(actual_text + "▌")
        container.markdown(actual_text)

        if sources_raw:
            st.divider()
            with st.expander("📚 Fontes e Documentos Originais", expanded=True):
            
                lines = sources_raw.strip().split("\n")
                cols = st.columns(2) 
                for idx, line in enumerate(lines):
                    if "|" in line:
                        name, url = line.split("|")
                        
                        cols[idx % 2].link_button(
                            f"📄 {name[:25]}...", 
                            url, 
                            use_container_width=True
                        )

      
        st.session_state.messages.append({"role": "assistant", "content": actual_text})