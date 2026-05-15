import shutil
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import CHUNKS_PATH, COLLECTION_NAME, UPLOADS_DIR
from src.pipeline import run_full_pipeline, run_index, run_ingest
from src.services.rag_service import RAGService
from src.vector_store import get_qdrant


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        info = get_qdrant().get_collection(COLLECTION_NAME)
        if getattr(info, "points_count", 0) == 0:
            raise ValueError("Collection is empty")
        print("✅ Collection already exists and has points, skipping auto-index.")
    except Exception:
        if CHUNKS_PATH.exists():
            print("⚡ Collection not found or empty — auto-indexing chunks...")
            run_index()
            print("✅ Auto-indexing complete.")
        else:
            print("⚠️  No chunks.json found. Run the full pipeline first.")
    yield


app = FastAPI(
    title="Egypt Law RAG API",
    description="Arabic legal Q&A with automated PDF ingestion pipeline",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGService()


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="Legal question in Arabic")
    top_k: int | None = Field(None, ge=1, le=20)


class QueryResponse(BaseModel):
    question: str
    answer: str
    citations: list[str]
    sources: list[dict]


class PipelineResponse(BaseModel):
    status: str
    message: str
    details: dict | None = None


@app.get("/health")
def health():
    return rag.health_check()


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        return rag.query(req.question, top_k=req.top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/pipeline/ingest", response_model=PipelineResponse)
def pipeline_ingest():
    try:
        result = run_ingest()
        return PipelineResponse(
            status="completed",
            message=f"Ingested {result['chunk_count']} chunks",
            details=result,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/pipeline/index", response_model=PipelineResponse)
def pipeline_index():
    try:
        result = run_index()
        return PipelineResponse(
            status="completed",
            message=f"Indexed {result['indexed_count']} chunks",
            details=result,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/pipeline/full", response_model=PipelineResponse)
def pipeline_full(background_tasks: BackgroundTasks, background: bool = False):
    if background:
        background_tasks.add_task(run_full_pipeline)
        return PipelineResponse(status="started", message="Full pipeline started in background")
    try:
        result = run_full_pipeline()
        return PipelineResponse(status="completed", message="Full pipeline completed", details=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/documents/upload", response_model=PipelineResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    law_name: str = "قانون العقوبات المصري",
    background: bool = True,
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    dest = UPLOADS_DIR / file.filename

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if background:
        background_tasks.add_task(run_full_pipeline, pdf_path=dest, law_name=law_name)
        return PipelineResponse(
            status="started",
            message=f"Pipeline started for {file.filename}",
            details={"pdf_path": str(dest), "law_name": law_name},
        )

    try:
        result = run_full_pipeline(pdf_path=dest, law_name=law_name)
        return PipelineResponse(
            status="completed",
            message=f"Pipeline completed for {file.filename}",
            details=result,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
