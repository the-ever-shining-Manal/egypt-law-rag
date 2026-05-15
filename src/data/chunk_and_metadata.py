import re
import json


def get_article_number(text):
    """Extract article number from article text."""
    match = re.search(r'مادة\s*[\[\(]?\s*(\d+)', text)
    if match:
        return int(match.group(1))
    return None


def detect_chapter(text):

    return "غير محدد"


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


if __name__ == "__main__":
    # Load articles from previous step
    import sys

    sys.path.append(".")
    from structure import extract_articles

    with open("C:\multi-agents\egypt-law-rag\data\cleaned_text.txt", "r", encoding="utf-8") as f:
        text = f.read()


    pattern = r'(مادة\s*[\[\(]?\s*\d+[\]\)]?\s*(?:مكررًا|مكرر|مكررا)?(?:\s*[\(\[]\s*\d*\s*[\)\]])?\s*.*?)(?=مادة\s*[\[\(]?\s*\d+|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    articles = [m.strip() for m in matches if len(m.strip()) > 30]

    chunks = build_chunks(articles)

    with open("C:\multi-agents\egypt-law-rag\output\chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(chunks)} chunks to output/chunks.json")
    print("\nSample chunk:")
    print(json.dumps(chunks[0], ensure_ascii=False, indent=2))