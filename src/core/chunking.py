def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list:

    if not text or len(text) <= chunk_size:
        return [text] if text else []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        chunks.append(chunk)
        
        start += chunk_size - chunk_overlap
    
    return chunks