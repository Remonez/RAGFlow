from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import settings
from core.document import extract_text

router = APIRouter()



@router.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running"
    }



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
        chunks = split_text(text, chunk_size=500, chunk_overlap=50)
        
        return {
            "filename": file.filename,
            "file_type": ext,
            "status": "processed",
            "char_count": len(text),
            "chunk_count": len(chunks),
            "first_chunk": chunks[0] if chunks else "No text",
            "sample_chunks": chunks[:3] if len(chunks) > 3 else chunks
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        file.file.close()

@router.get("/files")
async def list_files():
    files = [f.name for f in settings.UPLOAD_DIR.iterdir() if f.is_file()]
    return {"files": files, "count": len(files)}
