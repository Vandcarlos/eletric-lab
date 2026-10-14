from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer

from src.llm.state import AgentState


def detect_intent(state: AgentState) -> dict:
    # Deterministic bootstrap router. Replace with model-assisted classification later.
    requested = state.get("requested_type", "general")
    intent = "inspection" if requested == "inspection" else "general"
    return {"intent": intent}


def route(state: AgentState) -> str:
    return state["intent"]


def inspection_node(state: AgentState) -> dict:
    writer = get_stream_writer()
    chunks = [
        "Recebi sua solicitação de inspeção elétrica. ",
        "A análise visual por IA ainda não está habilitada. ",
        "Uma fotografia isolada não permite confirmar a segurança da instalação. ",
        "Para avaliar o circuito, precisamos da tensão, seção dos condutores, proteção e carga.",
    ]
    for chunk in chunks:
        writer({"event": "message.delta", "data": {"text": chunk}})
    # Future vision provider can return a persisted annotated image URL.
    # Only emit image.generated if a real image artifact exists.
    return {"response": "".join(chunks), "image_url": None}


def fallback_node(state: AgentState) -> dict:
    writer = get_stream_writer()
    text = "No momento, o agente atende solicitações do tipo inspection."
    writer({"event": "message.delta", "data": {"text": text}})
    return {"response": text, "image_url": None}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("detect_intent", detect_intent)
    graph.add_node("inspection", inspection_node)
    graph.add_node("fallback", fallback_node)
    graph.add_edge(START, "detect_intent")
    graph.add_conditional_edges(
        "detect_intent",
        route,
        {"inspection": "inspection", "general": "fallback"},
    )
    graph.add_edge("inspection", END)
    graph.add_edge("fallback", END)
    return graph.compile()


main_graph = build_graph()
