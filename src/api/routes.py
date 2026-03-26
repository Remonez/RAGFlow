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
    """
    Upload a document and extract text
    """
    # Validate file type
    allowed = [".pdf", ".txt"]
    ext = Path(file.filename).suffix.lower()
    
    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Only {allowed} allowed, got {ext}"
        )
    
    # Save file
    file_path = settings.UPLOAD_DIR / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text
        text = extract_text(file_path)
        
        # Preview: first 500 chars
        preview = text[:500] + "..." if len(text) > 500 else text
        
        return {
            "filename": file.filename,
            "file_type": ext,
            "status": "uploaded_and_processed",
            "char_count": len(text),
            "text_preview": preview
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        file.file.close()


@router.get("/files")
async def list_files():
    """List uploaded files"""
    files = [f.name for f in settings.UPLOAD_DIR.iterdir() if f.is_file()]
    return {"files": files, "count": len(files)}
