# Shopping Assistant Agent

AI-powered shopping assistant chatbot built with FastAPI, OpenAI Agents SDK, and Server-Sent Events for real-time streaming responses.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| AI Agent | OpenAI Agents SDK + LiteLLM |
| Database | SQLite (async via aiosqlite) |
| ORM | SQLModel |
| Migration | Alembic |
| Search | Tavily API |
| LLM Provider | OpenRouter |
| Package Manager | uv |

## Project Structure

```
.
├── alembic/                    # Database migrations
│   ├── env.py
│   └── versions/
├── app/
│   ├── core/
│   │   └── settings.py         # App configuration (env vars)
│   ├── models/
│   │   ├── database.py         # SQLModel table definitions
│   │   └── engine.py           # Async DB engine & get_db dependency
│   └── modules/
│       ├── agents/
│       │   ├── models.py       # LLM model configuration
│       │   ├── prompt.py       # System prompt
│       │   └── tools.py        # Agent tools (search, calculate)
│       ├── chats/
│       │   ├── router.py       # Chat streaming endpoint
│       │   └── schema.py       # Request/response schemas
│       └── sessions/
│           └── router.py       # Session CRUD endpoint
├── index.html                  # Chat UI
├── alembic.ini
├── pyproject.toml
└── .env
```

## Setup

```bash
# Clone & enter project
cd 05.FastAPI_agantStreaming

# Install dependencies
uv sync

# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
EOF

# Run database migrations
uv run alembic revision --autogenerate -m "init"
uv run alembic upgrade head

# Start server
uv run uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) to access the chat UI.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Chat UI (HTML) |
| `POST` | `/chats/` | Send message, receive SSE stream |
| `POST` | `/chat-sessions/` | Create new chat session |
| `GET` | `/scalar` | API documentation (Scalar) |

### POST /chats/

**Request:**
```json
{
  "session_id": "my-session",
  "message": "Find the best price for AirPods Pro"
}
```

**Response (SSE stream):**
```
data: {"type": "text_delta", "delta": "I"}

data: {"type": "text_delta", "delta": " can"}

data: {"type": "tool_call", "tool_name": "search_web", "argument": "AirPods Pro best price 2025"}
```

## Key Learnings

### 1. Streaming with Server-Sent Events (SSE)

Traditional REST APIs wait for the full response before sending it back. SSE allows **real-time token-by-token streaming** from the LLM to the browser, creating a "typing" effect like ChatGPT.

```python
# Server: yield events as they arrive
async def event_generator():
    async for event in runner.stream_events():
        yield f"data: {json.dumps({...})}\n\n"

return StreamingResponse(event_generator(), media_type="text/event-stream")
```

```javascript
// Client: read stream incrementally
const reader = res.body.getReader();
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    // process chunk...
}
```

### 2. OpenAI Agents SDK Architecture

The Agents SDK provides a structured way to build AI agents with tools. Key concepts:

- **Agent**: Defines the AI's persona, instructions, model, and available tools
- **Runner**: Executes the agent with streaming or non-streaming modes
- **Tools**: Python functions decorated with `@function_tool` that the agent can call
- **Stream Events**: Two main types:
  - `RawResponsesStreamEvent` - Raw token deltas from the LLM (`ResponseTextDeltaEvent`)
  - `RunItemStreamEvent` - Higher-level events like tool calls, message completions

### 3. Alembic with Async SQLAlchemy

Alembic runs migrations synchronously, but the app uses an async database engine (`aiosqlite`). The solution is to **strip the async driver prefix** in `alembic/env.py`:

```python
# App uses: sqlite+aiosqlite:///./agent.db
# Alembic needs: sqlite:///./agent.db
db_url = settings.DATABASE_URL.replace("+aiosqlite", "")
config.set_main_option("sqlalchemy.url", db_url)
```

This allows both the async app and sync Alembic to coexist without conflicts.

### 4. Model Abstraction with LiteLLM

Using `LitellmModel` from the Agents SDK allows switching between LLM providers (OpenAI, Gemini, Anthropic) by changing only the model name. However, **event compatibility varies by provider** - OpenAI's native response format is the most reliable for streaming, while some providers may not support token-level streaming through proxy services like OpenRouter.

### 5. SSE Client-Side Stream Parsing

Reading SSE in the browser requires careful buffer handling. Chunks may arrive mid-line or split across multiple `reader.read()` calls:

```javascript
let buffer = '';
while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    
    const lines = buffer.split('\n');
    buffer = lines.pop();  // Keep incomplete line
    
    for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const data = JSON.parse(line.slice(6));
        // handle event...
    }
}
```

## Make Commands

```bash
make dev      # Start dev server with hot reload
make format   # Format code with ruff
```

## License

MIT
