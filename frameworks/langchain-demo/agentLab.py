from langchain.agents import create_agent
from langchain_ollama import ChatOllama

# Import tools from customtools.py
from customtools import calculator, student_lookup


# ===================================================
# LLM
# ===================================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ===================================================
# TOOLS
# ===================================================

tools = [
    calculator,
    student_lookup
]


# ===================================================
# CREATE AGENT
# ===================================================

agent = create_agent(
    model=llm,
    tools=tools
)


# ===================================================
# CONVERSATION HISTORY
# ===================================================

messages = []


# ===================================================
# TURN 1
# ===================================================

messages.append({
    "role": "user",
    "content": "Look up Priya"
})

result1 = agent.invoke({
    "messages": messages
})

# Update conversation history
messages = result1["messages"]

print("\n=== TURN 1 ===")
print(messages[-1].content)


# ===================================================
# TURN 2
# ===================================================

messages.append({
    "role": "user",
    "content": "What is 10% of her CGPA?"
})

result2 = agent.invoke({
    "messages": messages
})

# Update conversation history
messages = result2["messages"]

print("\n=== TURN 2 ===")
print(messages[-1].content)


# ===================================================
# MEMORY / CONVERSATION HISTORY
# ===================================================

print("\n=== MEMORY ===")

for message in messages:
    print(f"[{message.type.upper()}] {message.content}")