from langgraph.graph import StateGraph, START, END

from src.llm.main.state import MainState
from src.llm.main.nodes.detect_intent import DetectIntentNode
from src.llm.main.nodes.fallback import FallbackNode
from src.llm.inspect.graph import inspect_graph


def route(state: MainState) -> str:
    return state["intent"]


def build_graph():
    graph = StateGraph(MainState)
    graph.add_node("detect_intent", DetectIntentNode())
    graph.add_node("inspect", inspect_graph)
    graph.add_node("fallback", FallbackNode())
    graph.add_edge(START, "detect_intent")
    graph.add_conditional_edges(
        "detect_intent", route, {"inspection": "inspect", "general": "fallback"}
    )
    graph.add_edge("inspect", END)
    graph.add_edge("fallback", END)
    return graph.compile()


main_graph = build_graph()
