import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

from src.config import OPENAI_API_KEY, CHAT_MODEL, DEFAULT_TOP_K, UPLOADS_DIR
from src.retriever import retrieve
from src.adapters import qdrant_hits_to_chunks
from src.generator import LegalAnswerGenerator
from src.pipeline import run_ingest, run_index, run_full_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=OPENAI_API_KEY)
generator = LegalAnswerGenerator(llm=client, model=CHAT_MODEL)


# ── Health ────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


# ── Query ─────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str
    top_k: int = DEFAULT_TOP_K

@app.post("/query")
def query(request: QueryRequest):
    hits = retrieve(request.question, top_k=request.top_k)
    chunks = qdrant_hits_to_chunks(hits)
    result = generator.generate_answer(request.question, chunks)

    # Shape sources to match what the frontend expects
    sources = [
        {
            "law": c["metadata"].get("law", "غير محدد"),
            "article": c["metadata"].get("article_number", "غير محدد"),
            "text_preview": c["text"][:200] if c.get("text") else "",
        }
        for c in chunks
    ]

    return {"answer": result["answer"], "sources": sources}


# ── Document Upload ───────────────────────────────────────
@app.post("/documents/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    law_name: str = Form(default="مستند مخصص"),
):
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    dest = UPLOADS_DIR / file.filename

    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    background_tasks.add_task(run_full_pipeline, pdf_path=dest, law_name=law_name)
    return {"message": f"جاري معالجة الملف: {file.filename}"}


# ── Pipeline Triggers ─────────────────────────────────────
@app.post("/pipeline/ingest")
def pipeline_ingest(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_ingest)
    return {"message": "بدأت عملية الاستخراج"}

@app.post("/pipeline/index")
def pipeline_index(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_index)
    return {"message": "بدأت عملية الفهرسة"}

@app.post("/pipeline/full")
def pipeline_full(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_full_pipeline)
    return {"message": "بدأت العملية الكاملة"}