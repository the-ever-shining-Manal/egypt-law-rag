from typing import Any


def qdrant_hit_to_chunk(hit: Any) -> dict:
    """Map a Qdrant search result to the chunk dict expected by LegalAnswerGenerator."""
    payload = hit.payload or {}
    return {
        "text": payload.get("text", ""),
        "metadata": {
            "law": payload.get("law", "غير محدد"),
            "article_number": payload.get("article", "غير محدد"),
            "source": payload.get("source", "غير محدد"),
            "language": payload.get("language", "ar"),
            "chunk_index": payload.get("chunk_index", 0),
        },
        "score": hit.score,
    }


def qdrant_hits_to_chunks(hits: list) -> list[dict]:
    return [qdrant_hit_to_chunk(hit) for hit in hits]
