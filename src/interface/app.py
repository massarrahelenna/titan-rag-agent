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

st.set_page_config(page_title="TITAN - Interface", page_icon="🤖",layout = "wide")

st.title("TITAN - Interface de Consulta")
st.markdown("Digite sua pergunta sobre os documentos e obtenha respostas baseadas na base de conhecimento do TITAN.")

with st.sidebar:
    st.header("Configurações")
    st.info(f"**Modelo:** Claude 4.6 Sonnet")
    st.info(f"**Contexto:** 1M tokens")
    st.success("Configurações carregadas com sucesso!")
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
