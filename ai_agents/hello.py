import ollama

# Send a single message to Qwen2.5
response = ollama.chat(
    model='tinyllama',
    messages=[
        {
            'role': 'user',
            'content': 'What is Artificial Intelligence? Explain in 3 sentences.'
        }
    ]
)

# Extract and print the AI reply
print("AI Response:")
print("-" * 40)
print(response['message'])
print("-" * 40)
print("Done!")