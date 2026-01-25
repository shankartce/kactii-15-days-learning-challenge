import ollama

def generate_response(prompt_text, model_name="llama3.2"):
    """
    Day 5: The "Hello World" of AI Engineering.
    """
    print(f"\n--- Sending Prompt: '{prompt_text}' ---")
    
    try:
        # 1. The API Call
        # We pass the model name and the message history
        response = ollama.chat(model=model_name, messages=[
            {
                'role': 'user',
                'content': prompt_text,
            },
        ])
        
        # 2. Extracting the "Intelligence"
        # The raw response is a complex object; we need just the content.
        ai_reply = response['message']['content']
        
        print(f"🤖 AI Response:\n{ai_reply}")
        print("-" * 30)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Tip: Make sure Ollama is running! (Run 'ollama serve' in a separate terminal)")

if __name__ == "__main__":
    # Test 1: clear instruction
    generate_response("Explain the concept of 'Recursion' in one sentence.")
    
    # Test 2: Creative task
    generate_response("Write a haiku about a Python developer.")