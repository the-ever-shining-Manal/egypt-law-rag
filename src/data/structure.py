import re


def extract_articles(text):

    pattern = r'(مادة\s*\d+.*?)(?=مادة\s*\d+|$)'

    matches = re.findall(pattern, text, re.DOTALL)

    articles = []
    for m in matches:
        m = m.strip()
        if len(m) > 50:
            articles.append(m)

    return articles


if __name__ == "__main__":

    with open(r"C:\multi-agents\egypt-law-rag\data\cleaned_text.txt", "r", encoding="utf-8") as f:
        text = f.read()


    articles = extract_articles(text)

    print(f"Found {len(articles)} articles")

    print("\n--- First 3 articles ---\n")
    for i, a in enumerate(articles[:3]):
        print(f"[{i + 1}]")
        print(a[:300])
        print("---")


    with open(r"C:\multi-agents\egypt-law-rag\data\articles.txt", "w", encoding="utf-8") as f:
        for i, a in enumerate(articles):
            f.write(f"=== Article {i + 1} ===\n{a}\n\n")

    print("Saved articles.txt")