import json
from collections.abc import AsyncIterator
from uuid import uuid4

from src.api.agent_schemas import AgentRequest
from src.llm.main.graph import main_graph


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_agent(request: AgentRequest) -> AsyncIterator[str]:
    run_id = str(uuid4())
    yield sse("agent.started", {"run_id": run_id, "session_id": request.session_id})
    state = {
        "session_id": request.session_id,
        "requested_type": request.type.value,
        "message": request.message,
        "attachments": [item.model_dump() for item in request.attachments],
    }
    try:
        async for mode, chunk in main_graph.astream(
            state, stream_mode=["custom", "updates"], subgraphs=True
        ):
            if mode == "custom":
                # Non-subgraph implementations may return (mode, chunk).
                yield sse(chunk["event"], chunk["data"])
            elif mode == "updates":
                for node, update in chunk.items():
                    if node == "fallback" and isinstance(update, dict):
                        yield sse("agent.completed", {
                            "run_id": run_id,
                            "intent": "general",
                            "response": update.get("response", ""),
                        })
                    elif node == "inspect" and isinstance(update, dict):
                        if update.get("image_url"):
                            yield sse("image.generated", {
                                "url": update["image_url"], "mime_type": "image/png"
                            })
                        yield sse("agent.completed", {
                            "run_id": run_id,
                            "intent": "inspection",
                            "response": update.get("response", ""),
                        })
    except Exception:
        yield sse("agent.error", {
            "run_id": run_id, "message": "Falha ao executar o agente."
        })
