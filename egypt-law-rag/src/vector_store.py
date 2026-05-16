import json
import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

COLLECTION = "legal_articles"
VECTOR_SIZE = 1536


def get_qdrant() -> QdrantClient:
    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", "6333"))
    return QdrantClient(host=host, port=port)


def embed(text: str) -> list:
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def build_index() -> int:
    qdrant = get_qdrant()
    qdrant.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )

    chunks_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "chunks.json")

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Found {len(chunks)} chunks. Embedding now...")

    points = []
    for i, chunk in enumerate(chunks):
        vector = embed(chunk["text"])
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "law": chunk["metadata"].get("law", "unknown"),
                "article": chunk["metadata"].get("article_number", "unknown"),
                "source": chunk["metadata"].get("source", "unknown"),
                "language": chunk["metadata"].get("language", "unknown"),
                "chunk_index": chunk["metadata"].get("chunk_index", 0),
                "text": chunk["text"],
            }
        ))
        if (i + 1) % 10 == 0:
            print(f"  Embedded {i + 1}/{len(chunks)}")

    qdrant.upsert(collection_name=COLLECTION, points=points)
    print(f"Done. Indexed {len(points)} chunks into Qdrant.")
    return len(points)


if __name__ == "__main__":
    build_index()