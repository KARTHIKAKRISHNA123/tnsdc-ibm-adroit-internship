from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


# ===================================================
# LOAD LOCAL LLM
# ===================================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ===================================================
# CALCULATOR TOOL
# ===================================================

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression.
    Example: 2 + 2 * 3
    """

    expression = expression.replace("expression=", "")
    expression = expression.replace('"', "")
    expression = expression.replace("'", "")
    expression = expression.strip()

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as e:
        return f"Error: {e}"


# ===================================================
# STUDENT LOOKUP TOOL
# ===================================================

@tool
def student_lookup(name: str) -> str:
    """
    Look up a student by name.
    Returns department, CGPA, and risk level.
    """

    name = name.replace("name=", "")
    name = name.replace('"', "")
    name = name.replace("'", "")
    name = name.strip()

    db = {
        "Priya": "Dept: Cyber Security | CGPA: 9.1 | Risk: Low",
        "Arjun": "Dept: AI & ML | CGPA: 6.8 | Risk: Medium",
        "Deepika": "Dept: Data Science | CGPA: 8.5 | Risk: Low",
    }

    return db.get(
        name,
        f"Student '{name}' not found."
    )


# ===================================================
# TEST TOOLS DIRECTLY
# ===================================================

print("\n=== CALCULATOR TOOL TEST ===")

print(
    calculator.invoke({
        "expression": "(88+92+76+85+90)/5"
    })
)

print(
    calculator.invoke({
        "expression": "1/0"
    })
)


print("\n=== TOOL NAME ===")
print(calculator.name)


print("\n=== TOOL DESCRIPTION ===")
print(calculator.description)


print("\n=== STUDENT LOOKUP TOOL TEST ===")

print(
    student_lookup.invoke({
        "name": "Priya"
    })
)

print(
    student_lookup.invoke({
        "name": "Ravi"
    })
)


# ===================================================
# CREATE AGENT
# ===================================================

tools = [
    calculator,
    student_lookup
]

agent = create_agent(
    model=llm,
    tools=tools
)


# ===================================================
# RUN AGENT
# ===================================================

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is Priya's CGPA and 15% of it?"
        }
    ]
})


# ===================================================
# FINAL OUTPUT
# ===================================================

print("\n=== FINAL ANSWER ===")
print(result["messages"][-1].content)