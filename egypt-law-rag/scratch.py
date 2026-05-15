from src.retriever import retrieve
from src.generator import LegalAnswerGenerator
from src.config import CHAT_MODEL
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gen = LegalAnswerGenerator(llm=client, model=CHAT_MODEL)

query = "متى يعتبر القتل عمداً؟"
chunks = retrieve(query, top_k=5)
print("RETRIEVED CHUNKS:")
for i, c in enumerate(chunks):
    print(f"[{i+1}] Score: {c['score']}")
    print(f"Article: {c['metadata']['article_number']}, Text: {c['text'][:100]}")

print("\nGENERATING ANSWER...")
ans = gen.generate_answer(query, chunks)
print("ANSWER:")
print(ans["answer"])
