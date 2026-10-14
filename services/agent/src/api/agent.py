from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.api.agent_schemas import AgentRequest
from src.service.agent import stream_agent

router = APIRouter(prefix="/v1/agent", tags=["agent"])


@router.post("/stream")
async def agent_stream(request: AgentRequest) -> StreamingResponse:
    return StreamingResponse(
        stream_agent(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
        },
    )
