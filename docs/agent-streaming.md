# Agent streaming (SSE)

`POST /v1/agent/stream` accepts JSON:

```json
{
  "session_id": "session-123",
  "type": "inspection",
  "message": "Analise meu quadro",
  "attachments": [],
  "metadata": {}
}
```

Response: `text/event-stream`, with event/data pairs:

- `agent.started`: `{run_id, session_id}`
- `message.delta`: `{text}` (incremental content)
- `image.generated`: `{url, mime_type}` (only when a persisted artifact exists)
- `agent.completed`: `{run_id, intent, response}`
- `agent.error`: `{run_id, message}`

The initial LangGraph router trusts the explicit request type and routes to inspection or fallback.
It is not yet an LLM-based intent classifier. The inspection node streams deterministic
text chunks, not LLM tokens. There is no image generation, persistence, checkpointing
or authentication yet. `session_id` is correlation metadata, not persistent conversation state.
Image attachments are URL references but are not downloaded or inspected in this version.

Use `curl -N`:

```bash
curl -N http://localhost:8000/v1/agent/stream \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"demo","type":"inspection","message":"Analise este quadro"}'
```

For production: implement auth, tenant isolation, attachment allowlists/storage,
stream cancellation, timeout handling, image provenance, and checkpointing.
