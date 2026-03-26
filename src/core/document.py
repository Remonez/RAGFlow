from pathlib import Path
from PyPDF2 import PdfReader


def extract_text(file_path: Path) -> str:
    file_ext = file_path.suffix.lower()
    
    if file_ext == ".pdf":
        return extract_pdf(file_path)
    elif file_ext == ".txt":
        return extract_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def extract_pdf(file_path: Path) -> str:
    
    try:
      reader = PdfReader(str(file_path))
    except Exception as e:
        return f"Error reading PDF: {e}"

    text_parts = []
    
    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if text:
            text_parts.append(f"--- Page {page_num} ---\n{text}")
    
    full_text = "\n\n".join(text_parts)
    return full_text if full_text else "[No text extracted from PDF]"


def extract_txt(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()