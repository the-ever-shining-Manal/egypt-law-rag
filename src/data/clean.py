import re

def clean_arabic(text):
    text = re.sub(r'[ًٌٍَُِّْـ]', '', text)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


if __name__ == "__main__":
    with open(r"C:\multi-agents\egypt-law-rag\data\raw_text.txt", "r", encoding="utf-8") as f:
        raw = f.read()


    cleaned = clean_arabic(raw)


    with open(r"C:\multi-agents\egypt-law-rag\data\cleaned_text.txt", "w", encoding="utf-8") as f:
        f.write(cleaned)

    print("Cleaned text saved")
    print(cleaned[:500])