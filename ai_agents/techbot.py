import ollama

# System prompt defines the AI's personality and rules
SYSTEM_PROMPT = """You are TechBot, an expert AI assistant for computer science students.

Your personality:
- Friendly, encouraging, and patient
- Use simple language - avoid jargon unless explaining it
- Always give examples when explaining concepts
- If asked something outside tech, politely redirect to tech topics

Your expertise:
- Python programming
- Artificial Intelligence and Machine Learning
- Web Development (HTML, CSS, JavaScript)
- Data Science
- Cloud Computing and DevOps

Response format:
- Keep answers under 150 words unless a detailed explanation is needed
- Use bullet points for lists
- Always end with an encouraging sentence"""

# Start chat history with the system message
chat_history = [
    {'role': 'system', 'content': SYSTEM_PROMPT}
]

print("=" * 50)
print("    TechBot - Your AI Study Assistant")
print("=" * 50)
print("Powered by TinyLlama running locally on your PC")
print("Type 'exit' to quit\n")

while True:
    user_input = input("Student: ").strip()

    if user_input.lower() == "exit":
        print("\nKeep learning! You're doing great!")
        break

    if not user_input:
        continue

    chat_history.append({'role': 'user', 'content': user_input})

    print("\nTechBot is thinking...\n")

    response = ollama.chat(
        model='tinyllama',
        messages=chat_history
    )

    reply = response['message']['content']
    print("TechBot:", reply, "\n")

    chat_history.append({'role': 'assistant', 'content': reply})