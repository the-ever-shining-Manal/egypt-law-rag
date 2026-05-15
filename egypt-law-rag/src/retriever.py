from src.vector_store import get_qdrant, embed, COLLECTION


def retrieve(query: str, top_k: int = 5) -> list:
    qdrant = get_qdrant()
    query_vector = embed(query)

    results = qdrant.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    return [
        {
            "text": r.payload.get("text", ""),
            "metadata": {
                "law": r.payload.get("law", "غير محدد"),
                "article_number": r.payload.get("article", "غير محدد"),
                "source": r.payload.get("source", "غير محدد"),
                "language": r.payload.get("language", "ar"),
                "chunk_index": r.payload.get("chunk_index", 0),
            },
            "score": r.score,
        }
        for r in results
    ]