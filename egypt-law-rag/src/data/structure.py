import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def extract_articles(text: str) -> list:
    pattern = r'(مادة\s*\d+.*?)(?=مادة\s*\d+|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.strip() for m in matches if len(m.strip()) > 50]


if __name__ == "__main__":
    with open(DATA_DIR / "cleaned_text.txt", "r", encoding="utf-8") as f:
        text = f.read()

    articles = extract_articles(text)
    print(f"Found {len(articles)} articles")

    with open(DATA_DIR / "articles.txt", "w", encoding="utf-8") as f:
        for i, a in enumerate(articles):
            f.write(f"=== Article {i + 1} ===\n{a}\n\n")

    print("Saved articles.txt")
