import chromadb

_client = None
_collection = None


def get_client():
    global _client
    if _client is None:
        # New API: Simple persistent client
        _client = chromadb.PersistentClient(path="./chroma_db")
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        _collection = client.get_or_create_collection(name="documents")
    return _collection


def add_chunks(document_id: str, chunks: list, embeddings: list):

    collection = get_collection()
    
    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": document_id, "chunk_index": i} for i in range(len(chunks))]
    )
    
    return len(chunks)


def search(query_embedding: list, top_k: int = 3):

    collection = get_collection()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    output = []
    for i in range(len(results['ids'][0])):
        output.append({
            "text": results['documents'][0][i],
            "source": results['metadatas'][0][i]['source'],
            "score": float(results['distances'][0][i])
        })
    
    return output


def reset_db():
    client = get_client()
    try:
        client.delete_collection("documents")
    except:
        pass
    global _collection
    _collection = None
