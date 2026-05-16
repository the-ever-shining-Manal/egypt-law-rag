import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def clean_arabic(text: str) -> str:
    text = re.sub(r'[ًٌٍَُِّْـ]', '', text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_text():
    """Entry point called by pipeline.py"""
    raw_path = DATA_DIR / "raw_text.txt"
    cleaned_path = DATA_DIR / "cleaned_text.txt"

    with open(raw_path, "r", encoding="utf-8") as f:
        raw = f.read()

    cleaned = clean_arabic(raw)

    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"Cleaned text saved to {cleaned_path}")
    return cleaned


if __name__ == "__main__":
    clean_text()
