from openai import OpenAI

from src.config import CHAT_MODEL, DEFAULT_TOP_K, OPENAI_API_KEY
from src.generator import LegalAnswerGenerator
from src.retriever import retrieve


class RAGService:
    """Orchestrates retrieval + generation into one query flow."""

    def __init__(self, model: str | None = None, top_k: int | None = None):
        self.model = model or CHAT_MODEL
        self.top_k = top_k or DEFAULT_TOP_K
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self._generator = LegalAnswerGenerator(llm=self._client, model=self.model)

    def query(self, question: str, top_k: int | None = None) -> dict:
        k = top_k or self.top_k
        chunks = retrieve(question, top_k=k)
        result = self._generator.generate_answer(question, chunks)

        sources = [
            {
                "law": c["metadata"].get("law"),
                "article": c["metadata"].get("article_number"),
                "text_preview": c["text"][:200],
                "score": c.get("score"),
            }
            for c in chunks
        ]

        return {
            "question": question,
            "answer": result["answer"],
            "citations": result["citations"],
            "sources": sources,
        }

    @staticmethod
    def health_check() -> dict:
        from src.config import CHUNKS_PATH, COLLECTION_NAME, QDRANT_PATH
        from src.vector_store import get_qdrant

        ok = bool(OPENAI_API_KEY)
        collection_exists = False
        point_count = 0

        try:
            info = get_qdrant().get_collection(COLLECTION_NAME)
            collection_exists = True
            point_count = info.points_count or 0
        except Exception:
            pass

        return {
            "openai_configured": ok,
            "qdrant_path": str(QDRANT_PATH),
            "collection": COLLECTION_NAME,
            "collection_exists": collection_exists,
            "point_count": point_count,
            "chunks_file_exists": CHUNKS_PATH.exists(),
        }
