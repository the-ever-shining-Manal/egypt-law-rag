import re
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"


def get_article_number(text):
    match = re.search(r'مادة\s*[\[\(]?\s*(\d+)', text)
    if match:
        return int(match.group(1))
    return None


def build_chunks(articles, law_name="قانون العقوبات المصري"):
    chunks = []
    for i, article_text in enumerate(articles):
        article_num = get_article_number(article_text)
        chunk = {
            "id": i + 1,
            "text": article_text,
            "metadata": {
                "article_number": article_num,
                "law": law_name,
                "source": "قانون رقم 58 لسنة 1937",
                "language": "ar",
                "chunk_index": i
            }
        }
        chunks.append(chunk)
    return chunks


def chunk_documents(law_name="قانون العقوبات المصري"):
    """Entry point called by pipeline.py"""
    cleaned_path = DATA_DIR / "cleaned_text.txt"

    with open(cleaned_path, "r", encoding="utf-8") as f:
        text = f.read()

    pattern = r'(مادة\s*[\[\(]?\s*\d+[\]\)]?\s*(?:مكررًا|مكرر|مكررا)?(?:\s*[\(\[]\s*\d*\s*[\)\]])?\s*.*?)(?=مادة\s*[\[\(]?\s*\d+|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    articles = [m.strip() for m in matches if len(m.strip()) > 30]

    chunks = build_chunks(articles, law_name=law_name)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    chunks_path = OUTPUT_DIR / "chunks.json"

    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(chunks)} chunks to {chunks_path}")
    return chunks


if __name__ == "__main__":
    chunk_documents()
