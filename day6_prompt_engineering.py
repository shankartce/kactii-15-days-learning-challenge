import ollama

def test_prompt(prompt_type, system_prompt, user_prompt):
    print(f"\n--- Testing: {prompt_type} ---")
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ])
        print(f"🤖 Response:\n{response['message']['content']}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Scenerio: We want to extract specific data from a messy email.
    
    messy_email = """
    Hi team, my server (ID: SRV-404) is smoking. Error code is 503. 
    It happened at 10:30 AM. Fix it fast! - Dave
    """

    # 1. The Lazy Prompt (Zero-Shot, No Context)
    # Result: Usually chatty, might miss details, formatting is random.
    test_prompt(
        "Lazy Prompt", 
        "You are a helpful assistant.", 
        f"Extract info from this: {messy_email}"
    )

    # 2. The Engineered Prompt (Few-Shot + Structured System)
    # Result: Consistent JSON, no small talk, reliable for code.
    system_instruction = """
    You are an Incident Response classifier. 
    Your job is to extract server details into JSON format.
    Do not speak. Just output JSON.
    
    Example Input: "Server A1 is down."
    Example Output: {"id": "A1", "status": "down"}
    """
    
    test_prompt(
        "Engineered Prompt", 
        system_instruction, 
        f"Analyze this report: {messy_email}"
    )