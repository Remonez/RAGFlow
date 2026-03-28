import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    
    APP_NAME: str = os.getenv("APP_NAME")
    DEBUG: bool = os.getenv("DEBUG").lower() == "true"
    VERSION: str = os.getenv("VERSION")
    
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))
    
    UPLOAD_DIR: Path = Path(__file__).parent.parent / "uploads"


settings = Settings()

settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)