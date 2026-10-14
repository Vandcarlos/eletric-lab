from langgraph.config import get_stream_writer
from src.llm.main.state import MainState


class FallbackNode:
    def __call__(self, state: MainState) -> dict:
        message = "No momento, o agente atende solicitações do tipo inspection."
        get_stream_writer()({"event": "message.delta", "data": {"text": message}})
        return {"response": message, "image_url": None}
