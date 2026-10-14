from langgraph.config import get_stream_writer
from src.llm.inspect.state import InspectState


class InspectImageNode:
    def __call__(self, state: InspectState) -> dict:
        chunks = [
            "Recebi sua solicitação de inspeção elétrica. ",
            "A análise visual por IA ainda não está habilitada. ",
            "Uma fotografia isolada não permite confirmar a segurança da instalação. ",
            "Para avaliar o circuito, precisamos da tensão, seção dos condutores, proteção e carga.",
        ]
        writer = get_stream_writer()
        for chunk in chunks:
            writer({"event": "message.delta", "data": {"text": chunk}})
        return {
            "response": "".join(chunks),
            "image_url": None,
            "inspection_status": "needs_review",
        }
