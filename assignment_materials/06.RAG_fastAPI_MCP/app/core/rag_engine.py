import base64
import json
from pathlib import Path

import chromadb
from chonkie import OverlapRefinery, RecursiveChunker
from mistralai.client import Mistral
from openai import OpenAI

from app.core.settings import settings


# 1.Fungsi extract OCR
def extract_ocr_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using Mistral AI OCR.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text from the PDF

    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If OCR extraction fails
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Read and encode PDF to base64
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
        pdf_base64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    # Initialize Mistral client
    client = Mistral(api_key=settings.MISTRAL_API_KEY)

    # Call Mistral OCR API
    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{pdf_base64}",
        },
    )

    # Extract text from all pages
    extracted_text = ""
    for page in response.pages:
        extracted_text += page.markdown + "\n\n"

    return extracted_text.strip()


# 2. Fungsi chunking recursive dengan overlap
def chunk_text_recursive(
    text: str, chunk_size: int = 500, overlap: int = 50
) -> list[dict]:
    """Chunk text using recursive chunking with Chonkie.

    Args:
        text: Text to chunk (result from OCR extraction)
        chunk_size: Target chunk size in tokens (default: 500)
        overlap: Overlap size between chunks (default: 50)

    Returns:
        List of chunks with text and metadata
    """
    chunker = RecursiveChunker(
        tokenizer="character",
        chunk_size=chunk_size,
    )

    chunks = chunker(text)

    # Apply overlap refinery
    refinery = OverlapRefinery(
        tokenizer="character",
        context_size=overlap,
        mode="token",
        method="suffix",
    )

    chunks = refinery(chunks)  # type: ignore

    return [
        {
            "text": chunk.text,
            "token_count": chunk.token_count,
            "start_index": chunk.start_index,
            "end_index": chunk.end_index,
        }
        for chunk in chunks
    ]


# 3. Fungsi ekstraksi metadata dengan LLM
def extract_chunk_metadata_with_llm(chunk_text: str) -> dict:
    """Extract semantic metadata from chunk using LLM.

    Args:
        chunk_text: Text content of the chunk

    Returns:
        Dictionary containing extracted metadata
    """
    client = OpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
    )

    prompt = f"""Analisis teks berikut dan ekstrak metadata dalam format JSON.

Teks:
{chunk_text}

Berikan response dalam format JSON dengan field berikut:
- keywords: Array 3-5 kata kunci utama
- topics: Array 1-3 topik utama yang dibahas
- language: Bahasa teks ("id" untuk Indonesia, "en" untuk English)

Response hanya JSON saja, tanpa markdown atau penjelasan tambahan."""

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten yang ahli dalam ekstraksi metadata dokumen. "
                    "Selalu response dalam format JSON yang valid."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=500,
    )

    result = response.choices[0].message.content

    try:
        metadata = json.loads(result)  # type: ignore
    except json.JSONDecodeError:
        metadata = {
            "keywords": [],
            "topics": [],
            "language": "unknown",
        }

    return metadata


# 4. Fungsi generate embeddings
def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of texts using OpenAI.

    Args:
        texts: List of text strings to embed

    Returns:
        List of embedding vectors
    """
    client = OpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
    )

    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=texts,
    )

    return [item.embedding for item in response.data]


# 5. Fungsi insert chunks ke ChromaDB
def insert_chunks_to_chromadb(
    chunks: list[dict],
    collection_name: str = "documents",
    persist_directory: str = "./chroma_db",
) -> dict:
    """Insert document chunks with metadata into ChromaDB.

    Args:
        chunks: List of enriched chunks with metadata
        collection_name: Name of the ChromaDB collection
        persist_directory: Directory to persist ChromaDB data

    Returns:
        Dictionary with insertion result info
    """
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=persist_directory)

    # Get or create collection
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    # Prepare data for insertion
    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        chunk_id = (
            f"{chunk['metadata']['source_file']}_{chunk['metadata']['chunk_index']}"
        )
        ids.append(chunk_id)
        documents.append(chunk["text"])

        # Flatten metadata for ChromaDB (only primitive types)
        metadata = {
            "source_file": str(chunk["metadata"]["source_file"]),
            "source_path": str(chunk["metadata"]["source_path"]),
            "chunk_index": int(chunk["metadata"]["chunk_index"]),
            "chunk_position": float(chunk["metadata"]["chunk_position"]),
            "token_count": int(chunk["token_count"]),
            "keywords": json.dumps(chunk["metadata"].get("keywords", [])),
            "topics": json.dumps(chunk["metadata"].get("topics", [])),
            "language": str(chunk["metadata"].get("language", "unknown")),
        }
        metadatas.append(metadata)

    # Generate embeddings
    embeddings = generate_embeddings(documents)

    # Insert into ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,  # type: ignore
        metadatas=metadatas,
    )

    return {
        "collection_name": collection_name,
        "total_inserted": len(ids),
        "persist_directory": persist_directory,
    }


# 6. Fungsi search dokumen relevan dengan metadata matching
def search_documents(
    query: str,
    collection_name: str = "documents",
    persist_directory: str = "./chroma_db",
    top_k: int = 5,
) -> list[dict]:
    """Search for relevant documents using similarity search with metadata boosting.

    Args:
        query: Search query text
        collection_name: Name of the ChromaDB collection
        persist_directory: Directory where ChromaDB data is stored
        top_k: Number of results to return (default: 5)

    Returns:
        List of relevant documents with normalized similarity scores and metadata
    """
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=persist_directory)

    # Get collection
    collection = client.get_collection(name=collection_name)

    # Generate query embedding
    query_embedding = generate_embeddings([query])[0]

    # Search more results for re-ranking with metadata
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k * 2,
        include=["documents", "metadatas", "distances"],
    )

    # Process results
    result_ids = results["ids"][0]  # type: ignore
    documents = results["documents"][0]  # type: ignore
    metadatas = results["metadatas"][0]  # type: ignore
    distances = results["distances"][0]  # type: ignore

    # Calculate similarity scores
    if len(distances) > 1:
        min_dist = min(distances)
        max_dist = max(distances)
        dist_range = max_dist - min_dist

        if dist_range > 0:
            similarity_scores = [1 - ((d - min_dist) / dist_range) for d in distances]
        else:
            similarity_scores = [1.0] * len(distances)
    else:
        similarity_scores = [1.0] if distances else []

    # Boost scores based on keyword/topic matching
    query_lower = query.lower()

    scored_results = []
    for i, (doc_id, doc, meta, sim_score) in enumerate(
        zip(result_ids, documents, metadatas, similarity_scores, strict=False)
    ):
        keywords = json.loads(meta.get("keywords", "[]"))
        topics = json.loads(meta.get("topics", "[]"))

        # Calculate metadata match boost
        keyword_matches = sum(
            1
            for kw in keywords
            if kw.lower() in query_lower or query_lower in kw.lower()
        )
        topic_matches = sum(
            1
            for topic in topics
            if topic.lower() in query_lower or query_lower in topic.lower()
        )

        # Boost score: +0.1 per keyword match, +0.15 per topic match
        boost = (keyword_matches * 0.1) + (topic_matches * 0.15)
        final_score = min(sim_score + boost, 1.0)

        scored_results.append(
            {
                "id": doc_id,
                "score": round(final_score, 4),
                "text": doc,
                "metadata": {
                    "source_file": meta.get("source_file", ""),
                    "source_path": meta.get("source_path", ""),
                    "chunk_index": meta.get("chunk_index", 0),
                    "chunk_position": meta.get("chunk_position", 0.0),
                    "token_count": meta.get("token_count", 0),
                    "keywords": keywords,
                    "topics": topics,
                    "language": meta.get("language", "unknown"),
                },
            }
        )

    # Sort by final score and return top_k
    scored_results.sort(key=lambda x: x["score"], reverse=True)

    # Add rank
    search_results = []
    for i, result in enumerate(scored_results[:top_k]):
        result["rank"] = i + 1
        search_results.append(result)

    return search_results
