from langgraph.graph import StateGraph
from typing import TypedDict
from rag_tool import rag_tool
from serp_tool import serp_tool

class State(TypedDict):
    query: str
    route: str
    answer: str


def classify(state: State):
    q = state["query"].lower()

    is_debales = "debales" in q
    is_general = any(word in q for word in [
        "latest", "news", "trend", "what", "who"
    ])

    if is_debales and is_general:
        return {"route": "both"}
    elif is_debales:
        return {"route": "rag"}
    else:
        return {"route": "serp"}


def rag_node(state: State):
    raw = rag_tool(state["query"])
    return {"answer": format_answer(state["query"], raw)}


def serp_node(state: State):
    raw = serp_tool(state["query"])
    return {"answer": format_answer(state["query"], raw)}

def both_node(state: State):
    rag_ans = rag_tool(state["query"])
    serp_ans = serp_tool(state["query"])

    combined = rag_ans + "\n" + serp_ans

    return {"answer": format_answer(state["query"], combined)}


def router(state: State):
    return state["route"]


builder = StateGraph(State)

builder.add_node("classify", classify)
builder.add_node("rag", rag_node)
builder.add_node("serp", serp_node)
builder.add_node("both", both_node)

builder.set_entry_point("classify")

builder.add_conditional_edges(
    "classify",
    router,
    {
        "rag": "rag",
        "serp": "serp",
        "both": "both"
    }
)

builder.set_finish_point("rag")
builder.set_finish_point("serp")
builder.set_finish_point("both")

graph = builder.compile()