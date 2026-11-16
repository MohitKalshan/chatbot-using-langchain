# Movie Information Extractor

Paste a paragraph about a movie. Gemini pulls out structured info (title, year, director, cast, …)
plus a short summary, and the result is saved to SQLite (`movies.db`). The same title and year
are never saved twice.

```bash
uv run python main.py
```

Needs `GOOGLE_API_KEY` in `.env`.

## Embeddings (first step toward RAG)

**What is an embedding?** A list of numbers that captures the *meaning* of a text. Texts with
similar meaning get similar numbers, so we can later find related movies by comparing vectors
instead of matching keywords. Example: "A thief steals secrets from dreams" and "A burglar takes
secrets from people while they sleep" score 0.60 similarity, while a cake recipe scores 0.12.

**Why `all-MiniLM-L6-v2`?** It's small (~90 MB), fast on a laptop CPU, free, runs locally with no
API key, and is a widely used default for semantic search on short texts like our summaries.

**Why 384 numbers?** That is the model's fixed output size (its hidden layer width). Every text,
short or long, becomes exactly 384 numbers, so all vectors can be compared with each other.

**How it works** (`src/project/services/embedding.py`):
- `generate_embedding(text)` rejects empty or whitespace-only text with `ValueError`.
- The model is loaded on the first call and cached, so later calls reuse it.
- Loading or encoding failures are raised as `RuntimeError` with a clear message.
- It returns a plain `list[float]` of length 384.

Embeddings are not stored yet; that comes with the vector database step.

### Try it

```bash
uv run python embed_movies.py   # embeds every saved summary; read-only, the database is not changed
uv run pytest -v                # unit tests; the model is mocked, so nothing is downloaded
```

The first `embed_movies.py` run downloads the model (~90 MB) into the Hugging Face cache.
