import ollama

print("-" * 45)
print("     TinyLlama Chatbot")
print("-" * 45)
print("Type your question and press Enter.")
print("Type 'exit' to quit.\n")

message_count = 0

while True:
    # Get input from user
    user_input = input("You: ").strip()

    # Exit condition
    if user_input.lower() in ["exit", "quit", "bye"]:
        print(f"👋 Goodbye! You asked {message_count} questions.")
        break

    # Skip empty input
    if not user_input:
        print("Please type something!\n")
        continue

    message_count += 1
    print(f"\nThinking... message #{message_count}\n")

    # Send to TinyLlama
    response = ollama.chat(
        model='tinyllama',
        messages=[
            {
                'role': 'user',
                'content': user_input
            }
        ]
    )

    # Extract AI response
    ai_response = response['message']['content']

    # Display AI response
    print("TinyLlama:", ai_response)
    print()