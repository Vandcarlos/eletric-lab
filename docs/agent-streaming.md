# Agent streaming

The only inspection entrypoint is `POST /v1/agent/stream`.

Request example:
```json
{"session_id":"demo","type":"inspection","message":"Analise meu quadro","attachments":[]}
```

SSE events: `agent.started`, `message.delta`, optional `image.generated`, `agent.completed`, `agent.error`.

Architecture:

```text
src/llm/
  main/
    graph.py
    state.py
    nodes/
      detect_intent.py
      fallback.py
  inspect/
    graph.py
    state.py
    nodes/
      inspect_image.py
```

Nodes are callable classes using `__call__`. Main and inspect have distinct state schemas.
The compiled inspect subgraph is mounted as a node inside the main graph.
Shared keys (`message`, `attachments`, `response`, `image_url`) pass between graphs;
`inspection_status` stays private to inspect.

The initial router is deterministic; no model is invoked. Image generation and analysis
are not implemented yet. Image URLs are references only and are not fetched.

The SSE stream should carry text chunks from nested graph nodes, with one terminal
completion event from the parent graph.
