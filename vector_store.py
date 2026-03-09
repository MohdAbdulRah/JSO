"""
vector_store.py – ChromaDB Vector Store with SentenceTransformer Embeddings
Handles embedding generation and semantic similarity search for job matching.
"""

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Singleton-style globals (initialised lazily)
# ---------------------------------------------------------------------------
_client: chromadb.ClientAPI | None = None
_collection: chromadb.Collection | None = None
_embedder: SentenceTransformer | None = None

COLLECTION_NAME = "jso_jobs"
MODEL_NAME = "all-MiniLM-L6-v2"


def _get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(MODEL_NAME)
    return _embedder


def _get_collection() -> chromadb.Collection:
    global _client, _collection
    if _collection is None:
        _client = chromadb.Client()  # in-memory
        # Delete existing collection if it exists to avoid duplicates on re-run
        try:
            _client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        _collection = _client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def embed_text(text: str) -> list[float]:
    """Generate embedding for a single text string."""
    model = _get_embedder()
    return model.encode(text, show_progress_bar=False).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of texts."""
    model = _get_embedder()
    return model.encode(texts, show_progress_bar=False).tolist()


def index_jobs(jobs: list[dict]) -> int:
    """Embed and upsert all job descriptions into ChromaDB.

    Each job dict must contain at minimum: id, title, required_skills,
    description, experience_level, industry.

    Returns the number of documents indexed.
    """
    collection = _get_collection()

    ids = []
    documents = []
    metadatas = []

    for job in jobs:
        # Build a rich document combining all fields for better semantic match
        doc = (
            f"Job Title: {job['title']}. "
            f"Company: {job.get('company', 'N/A')}. "
            f"Industry: {job['industry']}. "
            f"Experience Level: {job['experience_level']}. "
            f"Required Skills: {', '.join(job['required_skills'])}. "
            f"Description: {job['description']}"
        )
        ids.append(job["id"])
        documents.append(doc)
        metadatas.append({
            "title": job["title"],
            "company": job.get("company", "N/A"),
            "industry": job["industry"],
            "experience_level": job["experience_level"],
            "required_skills": ", ".join(job["required_skills"]),
        })

    embeddings = embed_texts(documents)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    return len(ids)


def search_jobs(query_text: str, n_results: int = 5) -> dict:
    """Perform semantic search against the job collection.

    Returns a dict with keys: ids, documents, metadatas, distances.
    """
    collection = _get_collection()
    query_embedding = embed_text(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    return results


def reset():
    """Reset the vector store (useful for re-indexing)."""
    global _collection, _client
    _collection = None
    _client = None
