# =============================================================
# LAB 2 — AI-Powered Customer Support Router
# =============================================================

from typing import TypedDict

from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama
from rich.console import Console
from rich.panel import Panel


console = Console()


# -------------------------------------------------------------
# STEP 1: Connect to local Qwen model via Ollama
# -------------------------------------------------------------

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# -------------------------------------------------------------
# STEP 2: Define the State
# -------------------------------------------------------------

class SupportState(TypedDict):
    query: str        # Customer's original question
    category: str     # Classified category
    answer: str       # Final response from department agent


# -------------------------------------------------------------
# STEP 3: Classification Node
# -------------------------------------------------------------

def classify(state: SupportState) -> SupportState:
    """
    Uses Qwen to classify the customer query
    into billing, technical, or general.
    """

    prompt = f"""
You are a customer support classifier.

Classify the following customer query into exactly ONE category.

Query: {state['query']}

Rules:
- Reply with ONLY one word: billing, technical, or general
- Do NOT add explanations, punctuation, or extra words

billing = payment, invoice, refund, subscription, charges

technical = error, bug, crash, not working,
installation, login issues

general = hours, location, product information,
policies, student discounts, or other questions
"""

    result = llm.invoke(prompt)

    raw = result.content.strip().lower()

    # Safety check
    valid_categories = {
        "billing",
        "technical",
        "general"
    }

    if raw in valid_categories:
        state["category"] = raw
    else:
        state["category"] = "general"

    console.print(
        f"[bold cyan]Classified as: "
        f"{state['category'].upper()}[/bold cyan]"
    )

    return state


# -------------------------------------------------------------
# STEP 4: Department Agent Nodes
# -------------------------------------------------------------

def billing_agent(state: SupportState) -> SupportState:
    """
    Handles billing-related customer queries.
    """

    state["answer"] = (
        "BILLING SUPPORT\n"
        "Your query has been received by our Billing Team.\n"
        "Typical issues handled: payment failures, "
        "invoice disputes, refunds.\n"
        "Expected resolution: 24–48 hours.\n"
        "Reference: "
        + state["query"][:30]
        + "..."
    )

    return state


def technical_agent(state: SupportState) -> SupportState:
    """
    Handles technical customer queries.
    """

    state["answer"] = (
        "TECHNICAL SUPPORT\n"
        "Your query has been assigned to our Technical Team.\n"
        "Please provide: device type, OS version, "
        "error message screenshot.\n"
        "Expected resolution: 2–4 hours.\n"
        "Reference: "
        + state["query"][:30]
        + "..."
    )

    return state


def general_agent(state: SupportState) -> SupportState:
    """
    Handles general customer queries.
    """

    state["answer"] = (
        "GENERAL SUPPORT\n"
        "Thank you for contacting us.\n"
        "Our support team will get back to you shortly.\n"
        "Operating hours: Mon–Fri, 9 AM – 6 PM IST.\n"
        "Reference: "
        + state["query"][:30]
        + "..."
    )

    return state


# -------------------------------------------------------------
# STEP 5: Router Function
# -------------------------------------------------------------

def router(state: SupportState) -> str:
    """
    Reads the category from the state and
    returns the name of the next node.
    """

    return state["category"]


# -------------------------------------------------------------
# STEP 6: Build the LangGraph
# -------------------------------------------------------------

builder = StateGraph(SupportState)


# Add nodes
builder.add_node("classify", classify)
builder.add_node("billing", billing_agent)
builder.add_node("technical", technical_agent)
builder.add_node("general", general_agent)


# Add conditional routing
builder.add_conditional_edges(
    "classify",
    router,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general",
    }
)


# Starting node
builder.set_entry_point("classify")


# Ending nodes
builder.set_finish_point("billing")
builder.set_finish_point("technical")
builder.set_finish_point("general")


# Compile graph
graph = builder.compile()


# -------------------------------------------------------------
# STEP 7: Test Queries
# -------------------------------------------------------------

test_queries = [
    "My payment failed yesterday and I was charged twice",

    "The app crashes every time I try to login from my iPhone",

    "What are your office hours?",

    "I need a refund for my last invoice",

    "How do I reset my password? "
    "The reset email never arrives",

    "Do you offer student discounts?",
]


# -------------------------------------------------------------
# STEP 8: Run the Customer Support Router
# -------------------------------------------------------------

if __name__ == "__main__":

    console.print(
        "\n[bold magenta]"
        "=== AI Customer Support Router ==="
        "[/bold magenta]\n"
    )

    for query in test_queries:

        console.print(
            f"\n[bold white]Customer:[/bold white] {query}"
        )

        result = graph.invoke(
            {
                "query": query,
                "category": "",
                "answer": ""
            }
        )

        console.print(
            Panel(
                result["answer"],
                title=(
                    f"[bold green]"
                    f"Response ({result['category'].upper()})"
                    f"[/bold green]"
                ),
                border_style="green"
            )
        )

    console.print(
        "\n[bold yellow]"
        "All queries routed successfully."
        "[/bold yellow]"
    )