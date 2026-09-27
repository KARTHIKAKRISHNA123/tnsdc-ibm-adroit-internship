import ollama

print("=" * 50)
print("        Memory Chatbot")
print("=" * 50)
print("Type your question and press Enter.")
print("Type 'history' to see chat history.")
print("Type 'exit' or 'quit' to end.\n")

# This list stores the full conversation
chat_history = []

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("\nBye! Conversation ended.")
        break

    # Show the chat history on demand
    if user_input.lower() == "history":
        print("\n--- Chat History ---")
        for i, msg in enumerate(chat_history):
            role = "You" if msg['role'] == 'user' else "AI"
            print(f"{i+1}. {role}: {msg['content'][:80]}...")
        print("--------------------\n")
        continue

    if not user_input:
        continue

    # Add user message to history
    chat_history.append({
        'role': 'user',
        'content': user_input
    })

    print("\n[Thinking...]\n")

    # Send FULL history - this is what gives memory
    response = ollama.chat(
        model='gemma:2b',
        messages=chat_history
    )

    ai_reply = response['message']['content']
    print("AI:", ai_reply, "\n")

    # Add AI reply to history too
    chat_history.append({
        'role': 'assistant',
        'content': ai_reply
    })

    print(f"[Memory: {len(chat_history)} messages stored]\n")