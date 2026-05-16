import fitz
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def extract_pdf(pdf_path: Path | None = None):
    """Extract text from PDF and save to raw_text.txt"""
    pdf = pdf_path or DATA_DIR / "qanun_al_uqubat.pdf"

    doc = fitz.open(str(pdf))
    all_text = ""
    for page in doc:
        all_text += page.get_text() + "\n"
    doc.close()

    raw_path = DATA_DIR / "raw_text.txt"
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"Extracted text saved to {raw_path}")
    return all_text


if __name__ == "__main__":
    extract_pdf()
