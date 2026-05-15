import re

def clean_arabic(text):
    text = re.sub(r'[ًٌٍَُِّْـ]', '', text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


if __name__ == "__main__":
    # 1. Read extracted TEXT file (NOT PDF)
    with open(r"C:\multi-agents\egypt-law-rag\data\raw_text.txt", "r", encoding="utf-8") as f:
        raw = f.read()

    # 2. Clean it
    cleaned = clean_arabic(raw)

    # 3. Save cleaned output
    with open(r"C:\multi-agents\egypt-law-rag\data\cleaned_text.txt", "w", encoding="utf-8") as f:
        f.write(cleaned)

    print("Cleaned text saved")
    print(cleaned[:500])