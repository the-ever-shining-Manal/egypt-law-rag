import fitz  # PyMuPDF

doc = fitz.open("C:\multi-agents\egypt-law-rag\data\qanun_al_uqubat.pdf")

all_text = ""

for page in doc:
    all_text += page.get_text() + "\n"

with open(r"C:\multi-agents\egypt-law-rag\data\raw_text.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("raw_text.txt created successfully!")