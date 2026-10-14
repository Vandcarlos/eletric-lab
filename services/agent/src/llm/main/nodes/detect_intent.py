from src.llm.main.state import MainState


class DetectIntentNode:
    def __call__(self, state: MainState) -> dict:
        requested = state.get("requested_type", "general")
        return {"intent": "inspection" if requested == "inspection" else "general"}
