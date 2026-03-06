# Agentic Threat Intelligence Workflow

An AI-powered threat intelligence system that autonomously researches and generates professional security reports using agentic workflows.

## Overview

This project implements an **agentic workflow** for Cyber Threat Intelligence (CTI) analysis. It leverages Large Language Models (LLMs) and web search APIs to automatically:

1. Generate targeted search queries from a given topic
2. Search the web for relevant threat intelligence
3. Summarize and analyze the collected data
4. Generate professional threat intelligence reports in PDF format

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Server                           │
│                      (app/main.py)                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    POST /search-threat
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Celery Task Queue                            │
│                  (Redis Broker/Backend)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  find_threat_task                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Generate   │  │    Search    │  │   Generate   │         │
│  │   Queries    │──▶│   (Tavily)   │──▶│    Report    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                            │                   │               │
│                            ▼                   ▼               │
│                     ┌──────────────┐    ┌──────────────┐       │
│                     │   Summarize  │    │  PDF Output  │       │
│                     │  (LLM/AI)    │    │ (WeasyPrint) │       │
│                     └──────────────┘    └──────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| API Framework | FastAPI |
| Task Queue | Celery |
| Message Broker | Redis |
| Web Search | Tavily |
| AI Models | OpenRouter (DeepSeek, Qwen) |
| Web Scraping | Apify |
| PDF Generation | WeasyPrint |
| Python | 3.13+ |

## Project Structure

```
assignment_materials/04.agentic_workflow/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── celery_app.py              # Celery configuration
│   ├── modules/
│   │   └── threat/
│   │       ├── __init__.py
│   │       ├── schema.py          # Pydantic models
│   │       ├── tasks.py           # Celery tasks (workflow logic)
│   │       ├── methods.py         # Core business logic
│   │       └── prompt.py          # System prompts for LLMs
│   └── utils/
│       ├── __init__.py
│       ├── openai.py              # OpenRouter client
│       ├── tavily.py              # Tavily search client
│       └── apify.py               # Apify client
├── .env                           # Environment variables
├── pyproject.toml                 # Project dependencies
├── Makefile                       # Development commands
└── README.md                      # This file
```

## Installation

### Prerequisites

- Python 3.13+
- Redis server

### Setup

1. **Install dependencies:**

```bash
uv sync
```

2. **Configure environment variables:**

Create a `.env` file with the following:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

3. **Start Redis:**

```bash
redis-server
```

## Usage

### Running the API Server

```bash
make dev
# or
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Running the Celery Worker

```bash
make celery
# or
uv run celery -A app.celery_app worker --loglevel=info
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search-threat` | Submit a threat topic for analysis |
| GET | `/scalar` | Interactive API documentation (Scalar) |

### Submitting a Threat Search

```bash
curl -X POST http://localhost:8000/search-threat \
  -H "Content-Type: application/json" \
  -d '{"topic": "ransomware 2024"}'
```

## Agentic Workflow

The system implements a multi-step agentic workflow:

### Step 1: Query Generation
The system generates multiple targeted search queries based on the input topic using keywords like `exploit`, `vulnerability`, and `CVE`.

### Step 2: Web Search
Each query is executed against Tavily's search API with advanced search depth and raw content extraction.

### Step 3: AI Summarization
Search results are summarized using LLMs via OpenRouter (DeepSeek model), extracting key data, numbers, and sources.

### Step 4: Report Generation
The collected research context is processed through an LLM (Qwen model) with a structured CTI prompt to generate a comprehensive threat intelligence report.

### Step 5: PDF Export
The final report is converted to PDF format using WeasyPrint and saved as `ThreatReport.pdf`.

## Output Report Structure

The generated threat intelligence report includes:

1. **Report Title**
2. **Executive Summary** - Key threat overview and recommended actions
3. **Threat Overview** - Classification and targeting patterns
4. **Threat Actor Profile** - Attribution and motivation
5. **TTPs (MITRE ATT&CK)** - Tactics, Techniques, and Procedures
6. **IOCs** - Indicators of Compromise in table format
7. **Attack Infrastructure** - C2 and delivery methods
8. **Impact Assessment** - Business impact and severity
9. **Detection Opportunities** - SIEM and monitoring strategies
10. **Mitigation Recommendations** - Defensive controls
11. **Intelligence Gaps** - Areas for further investigation
12. **References** - Sources and advisories

## Development Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start FastAPI development server |
| `make celery` | Start Celery worker |

## License

MIT License
