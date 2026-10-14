from langgraph.graph import StateGraph, START, END
from src.llm.inspect.state import InspectState
from src.llm.inspect.nodes.inspect_image import InspectImageNode


def build_graph():
    graph = StateGraph(InspectState)
    graph.add_node("inspect_image", InspectImageNode())
    graph.add_edge(START, "inspect_image")
    graph.add_edge("inspect_image", END)
    return graph.compile()


inspect_graph = build_graph()
