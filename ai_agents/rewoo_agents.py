import ollama

MODEL = "qwen2.5:3b"


def ask_llm(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def planner(question):
    prompt = f"""
You are a planner.

Create exactly 3 simple steps to solve this question.

Question:
{question}

Return only:
1. ...
2. ...
3. ...
"""
    return ask_llm(prompt)


def worker(question, plan):
    prompt = f"""
You are the worker of an AI agent.

Question:
{question}

Plan:
{plan}

Execute the plan and find the important information
needed to answer the question.

Do not give a final answer yet.
"""
    return ask_llm(prompt)


def solver(question, plan, result):
    prompt = f"""
You are the final solver.

Question:
{question}

Plan:
{plan}

Worker result:
{result}

Now give the final answer clearly and briefly.
"""
    return ask_llm(prompt)


def main():
    print("=" * 50)
    print("        SIMPLE ReWOO AGENT")
    print("        Plan → Work → Solve")
    print("=" * 50)

    while True:

        question = input("\nAsk me: ")

        if question.lower() == "exit":
            break

        # --------------------
        # 1. PLAN
        # --------------------

        print("\n[PLANNER]")
        plan = planner(question)
        print(plan)

        # --------------------
        # 2. WORK
        # --------------------

        print("\n[WORKER]")
        result = worker(question, plan)
        print(result)

        # --------------------
        # 3. SOLVE
        # --------------------

        print("\n[SOLVER]")
        answer = solver(question, plan, result)

        print("\nFINAL ANSWER:")
        print(answer)


if __name__ == "__main__":
    main()