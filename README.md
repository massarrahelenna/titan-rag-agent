# 🤖 Projeto Titan
> **Agente de Inteligência Científica (RAG)**


O Projeto Titan é um ecossistema de inteligência artificial projetado para realizar análises técnicas profundas e sínteses de alta fidelidade a partir de grandes volumes de documentos científicos. Utilizando uma arquitetura de Geração Aumentada de Recuperação (RAG), o agente é capaz de "ler" e correlacionar informações entre dezenas de artigos simultaneamente, mantendo precisão absoluta e rastreabilidade de fontes.

---

## O que este Agente faz?

Este agente não apenas responde perguntas; ele atua como um Pesquisador Sênior Virtual:

* **Análise Multidocumento:** Processa até 50+ PDFs técnicos (ex: papers do arXiv) de uma só vez.
* **Contexto de 1 Milhão de Tokens:** Graças ao Claude 4.6 Sonnet, o agente mantém a "memória" de todo o repositório durante a análise, permitindo cruzamento de dados complexos.
* **Geração de Relatórios:** Cria sínteses estruturadas em Markdown sobre tendências, metodologias e lacunas de pesquisa.
* **Rastreabilidade (Citações):** Cada resposta inclui links diretos para os objetos no Amazon S3 de onde a informação foi extraída.

---

## 🏗️ Arquitetura do Sistema

O projeto utiliza uma esteira de dados serverless na AWS:

* **Frontend (Streamlit):** Interface de usuário para chat e upload de arquivos.
* **Backend (FastAPI):** Orquestrador que gerencia o fluxo de streaming e a lógica de agentes.
* **Vetorização:** Amazon Bedrock Knowledge Bases utilizando **Titan Text Embeddings v2.**
* **Processamento:** **Claude 4.6 Sonnet** via Inference Profile para máxima disponibilidade.

---

## 🛠️ Tech Stack
|Camada|Tecnologia|
|------|----------|
|Linguagem	|Python 3.12+|
|IA Foundation Model|	Anthropic Claude 4.6 Sonnet (Lançado em Fev/2026)|
|Orquestração de IA|	Amazon Bedrock|
|Backend Framework| FastAPI + Uvicorn (Streaming Engine)|
|Frontend Framework|Streamlit|
|Embeddings|	Amazon Titan Text Embeddings v2|
|Cloud Infrastructure|	AWS (S3, IAM, OpenSearch)|
|Interface de API|	Boto3 (AWS SDK for Python)|

---

## ⚙️ Configuração e Instalação

**Pré-requisitos**
* Conta AWS com acesso ao Amazon Bedrock e Claude 4.6 habilitado.
* Docker e Docker Compose instalados (com integração WSL2 ativa).

**Instalação**
### 1. Clonar o Repositório
```bash
git clone https://github.com/massarrahelenna/titan.git
cd titan
```
### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```
### 3. Configure suas variáveis de ambiente no arquivo `.env`:
```bash
AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=seu_segredo
AWS_REGION=us-east-1
KNOWLEDGE_BASE_ID=sua_chave
```
## 🚀 Como Executar
Você pode rodar o Agente Titan de duas formas:

### **Opção A: Via Docker (Recomendado 🐳)**
Esta opção sobe automaticamente o Backend e o Frontend em containers separados, já configurando a comunicação entre eles.
### Construir a imagem:
```bash
docker compose up --build
```
### Rodar o container:
```bash
docker run -p 8501:8501 --env-file .env titan-agent
```
* Interface (UI): `http://localhost:8501`
* API (Docs): `http://localhost:8000/docs`

### **Opção B: Localmente (Desenvolvimento)**
Se preferir rodar fora do Docker, você precisará de dois terminais:
### Ative seu ambiente virtual:
```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```
### Terminal 1 (Backend):
```bash
python src/api/main.py
```
### Terminal 2 (Frontend):
```bash
streamlit run src/interface/app.py
```

### 📈 Resultados Identificados
Em testes iniciais com a base de dados atual, o agente identificou com sucesso os seguintes pilares tecnológicos nos documentos:
* **Robótica Embodied:** Evolução de políticas para robôs humanoides.
* **LLM-as-a-Judge:** Automação da avaliação de modelos através de orquestração.
* **Benchmarking Eficiente:** Novas métricas para avaliação de performance em larga escala.

### 📂 Fluxo de Upload e Ingestão
O sistema agora possui um pipeline automatizado para novos documentos:
* **Upload:** O usuário sobe um PDF via Streamlit.
* **S3 Storage:** O arquivo é salvo no prefixo raw_documents/ do seu bucket.
* **Auto-Sync:** O código dispara o start_ingestion_job no Amazon Bedrock.
* **Knowledge Update:** Em instantes, o Claude 4.6 já consegue responder sobre o novo conteúdo.
