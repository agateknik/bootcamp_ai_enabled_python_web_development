# RAG Engine - FastAPI & MCP

A Retrieval-Augmented Generation (RAG) engine built with **FastAPI** and **MCP (Model Context Protocol)**. This project processes PDF documents through OCR extraction, semantic chunking, LLM-based metadata enrichment, and stores them in ChromaDB for hybrid search with metadata boosting.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌───────────┐
│  PDF Input   │────▶│  Mistral OCR  │────▶│   Chonkie    │────▶│  LLM Meta  │
│  (URL/File)  │     │  Extraction   │     │  Chunking     │     │  Extraction │
└─────────────┘     └──────────────┘     └──────────────┘     └─────┬─────┘
                                                                    │
                                                                    ▼
                                                           ┌──────────────┐
                                                           │   ChromaDB    │
                                                           │  (Vector DB)  │
                                                           └──────┬───────┘
                                                                  │
                                         ┌───────────────────────┼───────────────────────┐
                                         │                       │                       │
                                         ▼                       ▼                       ▼
                                  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
                                  │ FastAPI Endp. │        │  MCP Tools   │        │ Hybrid Search │
                                  │  /upload      │        │  (External)   │        │  + Metadata   │
                                  │  /documents   │        │               │        │   Boosting    │
                                  │  /search      │        │               │        │               │
                                  └─────────────┘        └─────────────┘        └─────────────┘
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | FastAPI | REST API endpoints |
| API Documentation | Scalar | Interactive API reference |
| OCR Engine | Mistral AI OCR | PDF text extraction |
| Text Chunking | Chonkie (RecursiveChunker + OverlapRefinery) | Document splitting with overlap |
| Embedding Model | OpenAI text-embedding-3-small (via OpenRouter) | Vector embeddings |
| LLM | OpenAI GPT-4o-mini (via OpenRouter) | Metadata extraction |
| Vector Database | ChromaDB | Document storage & similarity search |
| MCP Server | FastMCP | External tool integration |

## Project Structure

```
.
├── app/
│   ├── core/
│   │   ├── rag_engine.py      # Core RAG functions (OCR, chunking, metadata, embeddings, search)
│   │   └── settings.py         # Configuration & environment variables
│   ├── modules/
│   │   ├── documents/
│   │   │   ├── router.py       # GET /documents endpoints
│   │   │   └── schema.py       # Document Pydantic models
│   │   ├── search/
│   │   │   ├── router.py       # GET /search endpoint
│   │   │   └── schema.py       # Search Pydantic models
│   │   └── upload/
│   │       ├── router.py       # POST /upload endpoint
│   │       ├── schema.py       # Upload Pydantic models
│   │       └── service.py      # PDF processing pipeline
│   └── main.py                 # FastAPI app & router registration
├── mcp_rag.py                  # MCP server wrapping RAG functions as tools
├── .env                        # Environment variables
├── pyproject.toml              # Python dependencies
└── Makefile                    # Development commands
```

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd 06.RAG_fastAPI_MCP

# Install dependencies
uv sync

# Copy environment file
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

```env
OPENROUTER_API_KEY=<your-openrouter-api-key>
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MISTRAL_API_KEY=<your-mistral-api-key>
```

### Running the API

```bash
# Development mode
make dev

# Or directly
uv run uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

Scalar documentation at `http://localhost:8000/scalar`

### Running the MCP Server

```bash
# Run MCP server
uv run mcp_rag.py
```

## API Endpoints

### Upload PDF

```http
POST /upload
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "chunk_size": 500,
  "overlap": 50,
  "collection_name": "documents"
}
```

### Search Documents

```http
GET /search?q=machine+learning&top_k=5
```

### List Documents

```http
GET /documents?limit=100
```

### Get Document Detail

```http
GET /documents/{document_id}
```

---

## MCP Tools

The MCP server exposes these tools for external AI clients (Claude Desktop, etc.):

| Tool | Description |
|------|-------------|
| `upload_pdf_from_url` | Process PDF from URL: OCR → Chunk → Metadata → ChromaDB |
| `search_rag_documents` | Hybrid search with metadata boosting |
| `list_documents` | List all document chunks in ChromaDB |
| `get_document` | Get specific document chunk by ID |

### MCP Client Configuration

```json
{
  "mcpServers": {
    "rag-engine": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_rag.py"]
    }
  }
}
```

## How It Works

### 1. PDF Processing Pipeline

```
PDF URL → Download → Mistral OCR → Recursive Chunking (overlap) → LLM Metadata → ChromaDB
```

- **OCR**: Mistral AI extracts text from PDF
- **Chunking**: RecursiveChunker splits text with 50-token overlap for context continuity
- **Metadata**: GPT-4o-mini extracts `keywords`, `topics`, `language` per chunk
- **Storage**: Chunks + metadata + embeddings stored in ChromaDB with cosine similarity

### 2. Hybrid Search with Metadata Boosting

Search combines two signals:

1. **Embedding Similarity** - Cosine similarity between query and document embeddings
2. **Metadata Boosting** - Score boosted when query matches chunk keywords (+0.1) or topics (+0.15)

```python
final_score = similarity_score + (keyword_matches * 0.1) + (topic_matches * 0.15)
```

Results are sorted by `final_score` and top-k are returned.

---

## What I Learned From This Project

### RAG Pipeline Architecture

- RAG is more than just "search and retrieve" - it's a **full pipeline**: document ingestion → extraction → chunking → metadata enrichment → embedding → storage → search
- Each stage significantly affects retrieval quality. Skipping metadata extraction or overlap chunking degrades results noticeably

### OCR with Mistral AI

- Mistral OCR returns markdown-formatted text, which preserves document structure (headings, tables)
- Base64 encoding is used to send PDF content directly to the Mistral API without external URLs
- OCR quality directly impacts downstream chunking quality

### Chunking Strategy

- **RecursiveChunker** is more simple and stable than SemanticChunker
- **Overlap** between chunks is critical for RAG - without overlap, context at chunk boundaries is lost, leading to poor retrieval at those margins
- Smaller chunks (500 tokens) with overlap (50 tokens) provide better granularity for search

### Metadata Extraction with LLM

- LLM-extracted `keywords` and `topics` are much more valuable than raw text for search - they provide structured, semantic signals that embedding similarity alone misses

### Hybrid Search Design

- Embedding-only search misses domain-specific terminology that keywords capture perfectly
- Metadata boosting is a simple but effective re-ranking technique: `+0.1` per keyword match and `+0.15` per topic match
- Fetching `top_k * 2` results then re-ranking ensures good candidates aren't missed before boosting
- Min-max normalization of cosine distances to `[0, 1]` makes scores interpretable

### ChromaDB Integration

- ChromaDB requires metadata to be **primitive types only** (strings, ints, floats) - arrays like `keywords` and `topics` must be JSON-serialized
- When deserializing, these JSON strings need to be parsed back with `json.loads()`
- Using `PersistentClient` instead of in-memory keeps data across restarts

### MCP Integration

- MCP (Model Context Protocol) wraps existing Python functions as tools that AI clients like Claude Desktop can call directly
- `FastMCP` makes it straightforward - just decorate functions with `@mcp.tool()` and provide clear docstrings
- All MCP tools return JSON strings since MCP transports data as text

### API Design Patterns

- Separating `service.py` from `router.py` keeps business logic testable and reusable across FastAPI and MCP
- Pydantic schemas in `schema.py` provide validation and auto-generated documentation
- Using `OpenRouter` as a proxy avoids managing multiple API keys for OpenAI models

---

## License

MIT