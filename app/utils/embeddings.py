import chromadb
from chromadb.config import Settings
from app.config import CHROMA_PERSIST_DIRECTORY
import os

def get_chroma_client():
    # Create directory if it doesn't exist
    os.makedirs(CHROMA_PERSIST_DIRECTORY, exist_ok=True)
    
    client = chromadb.PersistentClient(
        path=CHROMA_PERSIST_DIRECTORY,
        settings=Settings(anonymized_telemetry=False)
    )
    return client

def get_or_create_collection(collection_name="exam_prep"):
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def add_syllabus_to_vector_db(syllabus_id: int, content: str, topics: list):
    collection = get_or_create_collection()
    
    # Split content into semantic chunks
    sentences = content.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk + sentence) < 1000:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{"syllabus_id": syllabus_id, "chunk_id": i, "topics": str(topics)}],
            ids=[f"syllabus_{syllabus_id}_chunk_{i}"]
        )

def search_similar_content(query: str, n_results: int = 5):
    collection = get_or_create_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results