from PyPDF2 import PdfReader
from keybert import KeyBERT

def extract_text_from_pdf(pdf_path, skip_start=4, skip_end=1):
    reader = PdfReader(pdf_path)
    full_text = ""
    
    total_pages = len(reader.pages)
    start_idx = skip_start
    end_idx = total_pages - skip_end

    for page_num in range(start_idx, end_idx):
        try:
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                full_text += f"\n\n--- Page {page_num + 1} ---\n{text}"
        except Exception as e:
            print(f"Error reading page {page_num + 1}: {e}")

    return full_text

# 使用範例
pdf_path = "481987918-WF-Employee-handbook-pdf.pdf"
text_content = extract_text_from_pdf(pdf_path)

# 儲存內容到 text.txt
with open("text.txt", "w", encoding="utf-8") as f:
    f.write(text_content)

# 抽取關鍵字
kw_model = KeyBERT()
keywords = kw_model.extract_keywords(text_content, top_n=100)


with open("keyword.txt", "w", encoding="utf-8") as f:
    for word, score in keywords:
        f.write(f"{word}: {score:.4f}\n")
