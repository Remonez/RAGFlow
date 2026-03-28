# Docker Deployment for RAGFlow

Run RAGFlow with Docker Compose (App + ChromaDB).

## Quick Start

```bash
# 1. Go to docker folder
cd docker

# 2. Copy environment template
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 3. Build and run
docker-compose up --build

# 4. Open browser
# http://localhost:8000/docs