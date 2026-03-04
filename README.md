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

O projeto utiliza uma esteira de dados serverless na AWS para garantir escalabilidade e baixo custo:
* **Ingestão:** Scripts em Python monitoram e enviam documentos para o Amazon S3.
* **Vetorização:** O **Amazon Bedrock Knowledge Bases** utiliza o modelo **Titan Text Embeddings v2** para converter texto em vetores semânticos.
* **Armazenamento:** Os vetores são indexados em um banco de dados **Vector Store** (OpenSearch Serverless).
* **Orquestração & Inferência::** O **Claude 4.6 Sonnet** processa as consultas através de um **Inference Profile** cross-region para máxima disponibilidade.

---

## 🛠️ Tech Stack
|Camada|Tecnologia|
|------|----------|
|Linguagem	|Python 3.12+|
|IA Foundation Model|	Anthropic Claude 4.6 Sonnet (Lançado em Fev/2026)|
|Orquestração de IA|	Amazon Bedrock|
|Embeddings|	Amazon Titan Text Embeddings v2|
|Cloud Infrastructure|	AWS (S3, IAM, OpenSearch)|
|Interface de API|	Boto3 (AWS SDK for Python)|
