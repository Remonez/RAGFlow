# RAGFlow - Intelligent Document Q&A API

RAGFlow is a robust Retrieval-Augmented Generation (RAG) system designed to provide intelligent question-answering capabilities over your private documents. It leverages FastAPI for a high-performance backend, ChromaDB for vector storage, and Google Gemini for sophisticated natural language generation.

---

## 🚀 Features

- **Multi-format Document Support**: Seamlessly ingest `.pdf` and `.txt` files.
- **Intelligent Chunking**: Automatic text splitting with overlap to maintain context.
- **High-Performance Vector Search**: Powered by ChromaDB and `all-MiniLM-L6-v2` embeddings.
- **Gemini Integration**: Utilizing `gemini-3-flash` for fast and accurate context-aware responses.
- **Web Interface**: Simple built-in GUI to interact with the API directly.
- **Docker Ready**: Easy deployment using Docker and Docker Compose.

---


[🎥 Demo](https://github.com/user-attachments/assets/a6b575e7-d63e-41b6-8bca-bed514f1146c)


## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Google Gemini API Key**: [Get it here](https://aistudio.google.com/app/apikey)
- **Docker & Docker Compose** (Optional for containerized deployment)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Remonez/RAGFlow.git
cd RAGFlow
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Copy the `.env.example` file to `.env` and configure your API keys:

```bash
# Windows
copy src\.env.example src\.env

# Linux/macOS
cp src/.env.example src/.env
```

Open `src/.env` and update your `GEMINI_API_KEY`:


## 🚀 Running the Application

### Local Development
```bash
cd src
python main.py
```
The API will be available at `http://localhost:8000`.
- **API Docs**: `http://localhost:8000/docs`
- **Web GUI**: `http://localhost:8000/gui`

### Using Docker
```bash
docker-compose -f docker/docker-compose.yml up --build
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/upload` | Upload a PDF or TXT file for indexing. |
| `POST` | `/ask` | Ask a question based on uploaded documents. |
| `GET` | `/files` | List all uploaded documents. |
| `GET` | `/` | Health check and application info. |

---


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
