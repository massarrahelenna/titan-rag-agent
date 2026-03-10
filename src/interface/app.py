import streamlit as st
import boto3
from ask_knowledge import ask_titan_brain

st.set_page_config(page_title="TITAN - Interface", page_icon="🤖",layout = "wide")
st.title("TITAN - Interface de Consulta")
st.markdown("Digite sua pergunta sobre os documentos e obtenha respostas baseadas na base de conhecimento do TITAN.")

