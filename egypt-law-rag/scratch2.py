from src.vector_store import get_qdrant, COLLECTION
qdrant = get_qdrant()
info = qdrant.get_collection(collection_name=COLLECTION)
print(f"Collection: {COLLECTION}, Points count: {info.points_count}")
