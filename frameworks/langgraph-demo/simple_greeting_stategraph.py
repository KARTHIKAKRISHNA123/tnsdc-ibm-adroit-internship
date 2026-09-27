from typing import TypedDict
from langgraph.graph import StateGraph


# -------------------------------------------------------------
# STEP 1: Define the State
# -------------------------------------------------------------

class AgentState(TypedDict):
    name: str
    greeting: str


# -------------------------------------------------------------
# STEP 2: Define a Node
# -------------------------------------------------------------

def generate_greeting(state: AgentState) -> AgentState:
    """
    Node: Greeting Generator
    Reads 'name' from state, writes a greeting back.
    """
    name = state["name"]
    state["greeting"] = f"Welcome {name} to LangGraph Training!"
    return state


# -------------------------------------------------------------
# STEP 3: Build the Graph
# -------------------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("greet", generate_greeting)

builder.set_entry_point("greet")

builder.set_finish_point("greet")

graph = builder.compile()


# -------------------------------------------------------------
# STEP 4: Run the Graph
# -------------------------------------------------------------

if __name__ == "__main__":
    result = graph.invoke({"name": "Shyni"})
    print(result["greeting"])

    for name in ["Alice", "Bob", "VIT Student"]:
        output = graph.invoke({"name": name})
        print(output["greeting"])