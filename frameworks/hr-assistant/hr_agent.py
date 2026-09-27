from datetime import datetime
from typing import List

from pydantic import BaseModel

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.vectorstores import FAISS


# ==================================
# MODEL
# ==================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ==================================
# MEMORY
# ==================================

chat_history = InMemoryChatMessageHistory()


# ==================================
# LOAD VECTOR DB
# ==================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector_db = FAISS.load_local(
    "hr_vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)


# ==================================
# TOOLS
# ==================================

@tool
def experience_calculator(start_year: int) -> str:
    """Calculate candidate experience."""
    return str(datetime.now().year - start_year)


@tool
def eligibility_checker(skills: str) -> str:
    """Check candidate eligibility."""

    required = {
        "python",
        "sql",
        "git"
    }

    candidate = {
        skill.strip().lower()
        for skill in skills.split(",")
    }

    missing = required - candidate

    if len(missing) == 0:
        return "Eligible"

    return "Not Eligible. Missing: " + ", ".join(missing)


@tool
def company_policy_search(question: str) -> str:
    """
    Use this for leave, notice period, holidays, handbook,
    work-from-home, dress code, and other company policy questions.
    """

    docs = retriever.invoke(question)

    context = "\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = (
        "Use only the context provided below. "
        "If the answer is not in the context, "
        "say that the policy is not available in the documents.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}"
    )

    return llm.invoke(prompt).content


@tool
def interview_questions(skills: str) -> str:
    """Generate interview questions."""

    prompt = (
        f"Generate 5 interview questions for: {skills}"
    )

    return llm.invoke(prompt).content


tools = [
    experience_calculator,
    eligibility_checker,
    company_policy_search,
    interview_questions
]


# ==================================
# AGENT
# ==================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are an HR Recruitment Assistant. "
        "Use tools whenever required."
    )
)


# ==================================
# STRUCTURED OUTPUT
# ==================================

class Candidate(BaseModel):
    name: str
    experience: int
    skills: List[str]


structured_llm = llm.with_structured_output(
    Candidate
)


# ==================================
# CHAT LOOP
# ==================================

POLICY_KEYWORDS = (
    "leave",
    "casual",
    "sick",
    "earned",
    "notice",
    "policy",
    "handbook",
    "holiday",
    "attendance",
    "work from home",
    "dress code",
    "working hours"
)


def is_policy_question(question: str) -> bool:
    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in POLICY_KEYWORDS
    )


print("=" * 60)
print("HR RECRUITMENT ASSISTANT")
print("=" * 60)


resume = ""

messages = []


while True:

    user_input = input("\nYou : ").strip()

    if user_input.lower() == "exit":
        break


    # ==================================
    # RESUME PROCESSING
    # ==================================

    if user_input.lower().startswith("resume:"):

        resume = user_input.split(
            ":",
            1
        )[1].strip()

        if not resume:
            print(
                "\nPlease provide the resume text "
                "after 'resume:'"
            )
            continue


        candidate = structured_llm.invoke(
            f"""
Extract Name, Experience, Skills.

Resume:
{resume}
"""
        )

        print("\nCandidate Details")
        print(candidate)

        continue


    # ==================================
    # POLICY QUESTIONS
    # ==================================

    if is_policy_question(user_input):

        answer = company_policy_search.invoke(
            {
                "question": user_input
            }
        )

        print(
            "\nAssistant:",
            answer
        )

        continue


    # ==================================
    # NORMAL HR AGENT
    # ==================================

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    response = agent.invoke(
        {
            "messages": messages
        }
    )


    messages = response["messages"]


    print(
        "\nAssistant:",
        messages[-1].content
    )