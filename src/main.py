from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import settings
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from api.routes import router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

app.include_router(router)
app.mount("/gui", StaticFiles(directory=str(settings.STATIC_DIR), html=True), name="gui")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )