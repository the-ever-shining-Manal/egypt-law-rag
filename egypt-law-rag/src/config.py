import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
QDRANT_PATH = Path(os.getenv("QDRANT_PATH", PROJECT_ROOT / "qdrant_storage"))

PDF_PATH = DATA_DIR / "qanun_al_uqubat.pdf"
RAW_TEXT_PATH = DATA_DIR / "raw_text.txt"
CLEANED_TEXT_PATH = DATA_DIR / "cleaned_text.txt"
ARTICLES_PATH = DATA_DIR / "articles.txt"
CHUNKS_PATH = OUTPUT_DIR / "chunks.json"
UPLOADS_DIR = DATA_DIR / "uploads"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "legal_articles")
VECTOR_SIZE = 1536
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "5"))
