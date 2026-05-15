# import json
# import uuid
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams, PointStruct

# load_dotenv()

# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# qdrant = QdrantClient(path="./qdrant_storage")

# COLLECTION = "legal_articles"
# VECTOR_SIZE = 1536  


# # def embed(text: str) -> list:
# #     response = openai_client.embeddings.create(
# #         input=text,
# #         model="text-embedding-3-small"
# #     )
# #     return response.data[0].embedding

# #TESTING MODE YA NOURA
# import random
# def embed(text: str) -> list:
#     return [random.random() for _ in range(VECTOR_SIZE)]


# def build_index():
#     qdrant.recreate_collection(
#         collection_name=COLLECTION,
#         vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
#     )

#     with open("output/chunks.json", "r", encoding="utf-8") as f:
#      chunks = json.load(f)

#     print(f"Found {len(chunks)} chunks. Embedding now...")

#     points = []
#     for i, chunk in enumerate(chunks):
#         vector = embed(chunk["text"])
#         points.append(PointStruct(
#             id=str(uuid.uuid4()),
#             vector=vector,
#             payload={
#             "law": chunk["metadata"].get("law", "unknown"),
#             "article": chunk["metadata"].get("article_number", "unknown"),
#             "source": chunk["metadata"].get("source", "unknown"),
#             "language": chunk["metadata"].get("language", "unknown"),
#             "chunk_index": chunk["metadata"].get("chunk_index", 0),
#             "text": chunk["text"],
#         }
#         ))
#         if (i + 1) % 10 == 0:
#             print(f"  Embedded {i + 1}/{len(chunks)}")

#     qdrant.upsert(collection_name=COLLECTION, points=points)
#     print(f"Done. Indexed {len(points)} chunks into Qdrant.")


# if __name__ == "__main__":
#     build_index()

import random
from qdrant_client import QdrantClient

qdrant = QdrantClient(path="./qdrant_storage")

COLLECTION = "legal_articles"
VECTOR_SIZE = 1536


def embed(text: str):
    return [random.random() for _ in range(VECTOR_SIZE)]


def retrieve(query, top_k=3):
    query_vector = embed(query)

    results = qdrant.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
        limit=top_k
    )

    return results


if __name__ == "__main__":
    query = "هل يجوز فصل العامل؟"

    results = retrieve(query)

    print("\nTop Results:\n")

    for i, result in enumerate(results, 1):
        payload = result.payload

        print(f"Result #{i}")
        print(f"Law: {payload.get('law')}")
        print(f"Article: {payload.get('article')}")
        print(f"Score: {result.score}")
        print(f"Text: {payload.get('text')[:300]}")
        print("-" * 50)