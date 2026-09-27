# =============================================================
# AGENT CLIENT — LangGraph + Ollama + real MCP tool calling
#
# This agent:
#   1. Launches mcp_server.py as a subprocess and connects over stdio
#   2. Asks the MCP server "what tools do you have?" (session.list_tools)
#   3. Lets a local LLM (qwen2.5:3b) decide which tool + arguments fit
#   4. Calls the tool for real via session.call_tool() — no hardcoded
#      Python function calls, this goes through the actual MCP protocol
#   5. Synthesizes the raw tool result into a natural-language answer
# =============================================================

import asyncio
import json
from typing import TypedDict

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen2.5:3b", temperature=0)

# Launches: python mcp_server.py  (must be in the same folder)
SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["mcp_server.py"],
)


# -------------------------------------------------------------
# STATE
# -------------------------------------------------------------

class AgentState(TypedDict):
    query: str
    tools_description: str
    tool_name: str
    tool_args: dict
    tool_result: str
    final_answer: str


# -------------------------------------------------------------
# HELPER: format MCP tool list for the LLM prompt
# -------------------------------------------------------------

def format_tools_for_prompt(tools) -> str:
    lines = []
    for t in tools:
        params = (t.inputSchema or {}).get("properties", {})
        param_list = ", ".join(params.keys())
        lines.append(f"- {t.name}({param_list}): {t.description}")
    return "\n".join(lines)


# -------------------------------------------------------------
# NODE FACTORY — nodes need access to the live MCP session,
# so we build them as closures around that session.
# -------------------------------------------------------------

def make_decide_tool(session: ClientSession):
    async def decide_tool(state: AgentState) -> AgentState:
        prompt = f"""You are an assistant with access to these real tools:

{state['tools_description']}

User query: {state['query']}

Decide which ONE tool fits best, and what arguments to pass.
Respond with ONLY valid JSON, no explanation, no markdown:
{{"tool": "<tool_name>", "args": {{"param_name": "value"}}}}

If no tool truly fits, respond:
{{"tool": "none", "args": {{}}}}
"""
        result = llm.invoke(prompt)
        raw = result.content.strip().replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(raw)
            state["tool_name"] = parsed.get("tool", "none")
            state["tool_args"] = parsed.get("args", {})
        except json.JSONDecodeError:
            state["tool_name"] = "none"
            state["tool_args"] = {}

        print(f"LLM chose tool: {state['tool_name']} | args: {state['tool_args']}")
        return state

    return decide_tool


def make_call_tool(session: ClientSession):
    async def call_tool(state: AgentState) -> AgentState:
        if state["tool_name"] == "none":
            result = llm.invoke(state["query"])
            state["tool_result"] = result.content.strip()
            return state

        print(f"Calling MCP tool: {state['tool_name']} with {state['tool_args']}")

        response = await session.call_tool(state["tool_name"], state["tool_args"])

        # MCP results come back as a list of content blocks (usually text)
        text_parts = [block.text for block in response.content if hasattr(block, "text")]
        state["tool_result"] = "\n".join(text_parts) if text_parts else "No result returned."
        return state

    return call_tool


def synthesize(state: AgentState) -> AgentState:
    if state["tool_name"] == "none":
        state["final_answer"] = state["tool_result"]
        return state

    prompt = f"""Original question: {state['query']}
Tool result: {state['tool_result']}

Write a short, clear answer to the user using this result. 1-3 sentences.
"""
    result = llm.invoke(prompt)
    state["final_answer"] = result.content.strip()
    return state


# -------------------------------------------------------------
# MAIN AGENT RUN — one MCP session per query
# -------------------------------------------------------------

async def run_agent(query: str) -> str:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            tools_description = format_tools_for_prompt(tools_response.tools)

            builder = StateGraph(AgentState)
            builder.add_node("decide_tool", make_decide_tool(session))
            builder.add_node("call_tool", make_call_tool(session))
            builder.add_node("synthesize", synthesize)

            builder.add_edge("decide_tool", "call_tool")
            builder.add_edge("call_tool", "synthesize")
            builder.set_entry_point("decide_tool")
            builder.set_finish_point("synthesize")

            graph = builder.compile()

            result = await graph.ainvoke({
                "query": query,
                "tools_description": tools_description,
                "tool_name": "",
                "tool_args": {},
                "tool_result": "",
                "final_answer": "",
            })

            return result["final_answer"]


# -------------------------------------------------------------
# DEMO QUERIES
# -------------------------------------------------------------

queries = [
    "What's the weather like in Coimbatore right now?",
    "Convert 500 US dollars to Indian rupees",
    "Tell me some facts about Japan",
    "What's the capital of France?",  # tests the "none" / direct-answer path
]


async def main():
    print("\n=== Real-Time MCP Agent (LangGraph + Ollama + MCP) ===\n")
    for q in queries:
        print(f"\nQuery: {q}")
        answer = await run_agent(q)
        print("-" * 60)
        print("ANSWER:", answer)
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())