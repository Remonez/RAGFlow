from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings
from core.document import extract_text
from services.embeddings import embed_texts, embed_query
from services.vector_db import add_chunks, search
from services.llm import generate_answer


router = APIRouter()



@router.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running"
    }



@router.post("/ask")
async def ask(question: str):

    try:
        query_vec = embed_query(question)
        
        chunks = search(query_vec, top_k=3)
        
        if not chunks:
            return {
                "question": question,
                "answer": "No relevant documents found. Please upload documents first.",
                "sources": []
            }
        
        answer = generate_answer(question, chunks)
        
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "text": c["text"][:200] + "...",
                    "source": c["source"],
                    "relevance": round(c["score"], 3)
                }
                for c in chunks
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    allowed = [".pdf", ".txt"]
    ext = Path(file.filename).suffix.lower()
    
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Only {allowed} allowed, got {ext}"
        )
    
    file_path = settings.UPLOAD_DIR / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        text = extract_text(file_path)
        
        from core.chunking import split_text
        chunks = split_text(text, chunk_size=500, chunk_overlap=200)

        embeddings = embed_texts(chunks)
        
        doc_id = file.filename.replace(" ", "_")
        stored_count = add_chunks(doc_id, chunks, embeddings)
        
        return {
            "filename": file.filename,
            "file_type": ext,
            "status": "indexed",
            "char_count": len(text),
            "chunk_count": len(chunks),
            "stored_in_db": stored_count,
            "first_chunk_preview": chunks[0][:200] + "..." if chunks else "None"
        }        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        file.file.close()

@router.get("/files")
async def list_files():
    files = [f.name for f in settings.UPLOAD_DIR.iterdir() if f.is_file()]
    return {"files": files, "count": len(files)}
