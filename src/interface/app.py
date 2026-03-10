import streamlit as st
import boto3
import sys
import os
import time
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
sys.path.append(str(ROOT / "agents"))

from ask_knowledge import ask_titan_brain

s3_client = boto3.client('s3')
bedrock_agent = boto3.client('bedrock-agent') # Cliente para gerenciar a KB

def upload_to_s3(file_obj, bucket, s3_path):
    """Envia o arquivo para o S3"""
    try:
        s3_client.upload_fileobj(file_obj, bucket, s3_path)
        return True
    except Exception as e:
        st.error(f"Erro no S3: {e}")
        return False

def sync_knowledge_base(kb_id, ds_id):
    """Garante que a IA 'leia' o novo arquivo"""
    try:
        bedrock_agent.start_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=ds_id
        )
        return True
    except Exception as e:
        st.error(f"Erro na sincronização: {e}")
        return False

# --- INTERFACE STREAMLIT ---
with st.sidebar:
    st.header("📤 Upload de Documentos")
    uploaded_file = st.file_uploader("Escolha um PDF técnico", type="pdf")
    
    if uploaded_file is not None:
        if st.button("🚀 Enviar e Sincronizar"):
            with st.spinner("Enviando para o Titan Brain..."):
                # 1. Upload para o S3
                bucket_name = "titan-knowledge"
                success_s3 = upload_to_s3(uploaded_file, bucket_name, uploaded_file.name)
                
                if success_s3:
                    st.success(f"Arquivo {uploaded_file.name} salvo no S3!")
                    
                    # 2. Sincronizar Knowledge Base
                    # Substitua pelo seu Data Source ID (visto na image_4590c2.png)
                    ds_id = "ARSVWAGKQT" 
                    kb_id = "V9Y857FLPG"
                    
                    if sync_knowledge_base(kb_id, ds_id):
                        st.warning("🔄 Sincronização iniciada. A IA estará atualizada em instantes!")