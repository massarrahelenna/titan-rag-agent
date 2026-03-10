from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2] 
if str(ROOT / "src" / "agents") not in sys.path:
    sys.path.append(str(ROOT / "src" / "agents"))

from ask_knowledge import ask_titan_brain_stream

app = FastAPI(title="Titan API - Streaming Engine")

@app.get("/chat")
async def chat(prompt: str):
    """
    Endpoint que recebe o prompt via HTTP e devolve um 
    StreamingResponse (o texto 'digitando' em tempo real).
    """
    
    return StreamingResponse(ask_titan_brain_stream(prompt), media_type="text/plain")

if __name__ == "__main__":
    # Roda o servidor na porta 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)