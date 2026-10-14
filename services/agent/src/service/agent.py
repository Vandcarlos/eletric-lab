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
        completed = False
        async for namespace, mode, chunk in main_graph.astream(
            state, stream_mode=["custom", "updates"], subgraphs=True
        ):
            if mode == "custom" and isinstance(chunk, dict):
                yield sse(chunk["event"], chunk["data"])
            elif mode == "updates" and not namespace:
                for node, update in chunk.items():
                    if node not in ("inspect", "fallback") or not isinstance(update, dict):
                        continue
                    if update.get("image_url"):
                        yield sse("image.generated", {
                            "url": update["image_url"], "mime_type": "image/png"
                        })
                    yield sse("agent.completed", {
                        "run_id": run_id,
                        "intent": "inspection" if node == "inspect" else "general",
                        "response": update.get("response", ""),
                    })
                    completed = True
        if not completed:
            yield sse("agent.error", {
                "run_id": run_id, "message": "O agente terminou sem resposta."
            })
    except Exception:
        yield sse("agent.error", {
            "run_id": run_id, "message": "Falha ao executar o agente."
        })
