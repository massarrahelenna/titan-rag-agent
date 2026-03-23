# 🤖 Project Titan
> **Scientific Intelligence Agent (RAG)**

Project Titan is an artificial intelligence ecosystem designed to perform deep technical analysis and high-fidelity synthesis from large volumes of scientific documents. Using a Retrieval-Augmented Generation (RAG) architecture, the agent can "read" and correlate information across dozens of articles simultaneously, maintaining absolute accuracy and source traceability.

---

## What does this Agent do?

This agent does more than answer questions — it acts as a **Virtual Senior Researcher**:

- **Multi-Document Analysis:** Processes 50+ technical PDFs (e.g. arXiv papers) at once.
- **1 Million Token Context:** Powered by Claude Sonnet 4.6, the agent retains "memory" of the entire repository during analysis, enabling complex cross-referencing.
- **Report Generation:** Creates structured Markdown syntheses on research trends, methodologies, and knowledge gaps.
- **Traceability (Citations):** Every response includes direct links to the Amazon S3 objects from which the information was extracted.

---

## 🏗️ System Architecture

The project runs on a serverless AWS data pipeline:

- **Frontend (Streamlit):** User interface for chat and file uploads.
- **Backend (FastAPI):** Orchestrator that manages the streaming flow and agent logic.
- **Vectorization:** Amazon Bedrock Knowledge Bases using **Titan Text Embeddings v2**.
- **Processing:** **Claude Sonnet 4.6** via Inference Profile for maximum availability.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.12+ |
| AI Foundation Model | Anthropic Claude Sonnet 4.6 |
| AI Orchestration | Amazon Bedrock |
| Backend Framework | FastAPI + Uvicorn (Streaming Engine) |
| Frontend Framework | Streamlit |
| Embeddings | Amazon Titan Text Embeddings v2 |
| Cloud Infrastructure | AWS (S3, IAM, OpenSearch) |
| API Interface | Boto3 (AWS SDK for Python) |

---

## ⚙️ Setup & Installation

**Prerequisites**
- AWS account with access to Amazon Bedrock and Claude Sonnet 4.6 enabled.
- Docker and Docker Compose installed (with WSL2 integration active).

### 1. Clone the repository
```bash
git clone https://github.com/massarrahelenna/titan.git
cd titan
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your environment variables in the `.env` file
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
KNOWLEDGE_BASE_ID=your_key
```

---

## 🚀 How to Run

### **Option A: Via Docker (Recommended 🐳)**

Automatically starts the Backend and Frontend in separate containers with networking pre-configured.

```bash
# Build the image
docker compose up --build

# Run the container
docker run -p 8501:8501 --env-file .env titan-agent
```

- UI: `http://localhost:8501`
- API Docs: `http://localhost:8000/docs`

### **Option B: Locally (Development)**

Requires two separate terminals.

```bash
# Activate your virtual environment
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

```bash
# Terminal 1 — Backend
python src/api/main.py

# Terminal 2 — Frontend
streamlit run src/interface/app.py
```

---

## 📈 Identified Results

In initial tests with the current dataset, the agent successfully identified the following technology pillars across the documents:

- **Embodied Robotics:** Policy evolution for humanoid robots.
- **LLM-as-a-Judge:** Automated model evaluation through orchestration.
- **Efficient Benchmarking:** New metrics for large-scale performance evaluation.

---

## 📂 Upload & Ingestion Flow

The system features an automated pipeline for new documents:

1. **Upload:** User submits a PDF via Streamlit.
2. **S3 Storage:** The file is saved under the `raw_documents/` prefix in your bucket.
3. **Auto-Sync:** The code triggers `start_ingestion_job` on Amazon Bedrock.
4. **Knowledge Update:** Claude Sonnet 4.6 can answer questions about the new content within moments.

---

## 📂 Project Structure

```text
titan/
├── src/
│   ├── api/            # FastAPI server (Streaming)
│   ├── interface/      # Streamlit UI
│   └── agents/         # AWS Bedrock connection logic
├── requirements.txt    # Dependencies (boto3, fastapi, streamlit...)
└── docker-compose.yml  # Service orchestration
```
