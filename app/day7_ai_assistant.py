import ollama
import datetime

# Configuration
MODEL = "llama3.2"  # Ensure this matches your pulled model
LOG_FILE = "chat_history.log"

def save_log(role, text):
    """
    Saves conversation to a file with timestamps.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {role.upper()}: {text}\n")

def chat_bot():
    print(f"\n--- 🤖 Kactii AI Assistant (Model: {MODEL}) ---")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # 1. Initialize Conversation Memory (List of dicts)
    conversation_history = [
        {"role": "system", "content": "You are a helpful, concise AI assistant developed for the Kactii Challenge."}
    ]

    while True:
        # 2. Input Loop
        try:
            user_input = input("You: ")
            if not user_input.strip():
                continue
        except KeyboardInterrupt:
            print("\n🤖 AI: Force exit detected. Goodbye!")
            break
        
        # 3. Exit Condition
        if user_input.lower() in ["exit", "quit"]:
            print("🤖 AI: Goodbye! Session logged.")
            break
            
        # 4. Add User Input to Memory & Log
        conversation_history.append({"role": "user", "content": user_input})
        save_log("user", user_input)

        try:
            # 5. The Brain (LLM Call)
            print("Thinking...", end="\r")
            response = ollama.chat(model=MODEL, messages=conversation_history)
            ai_reply = response['message']['content']
            
            # 6. Output & Log
            print(f"🤖 AI: {ai_reply}\n")
            conversation_history.append({"role": "assistant", "content": ai_reply})
            save_log("ai", ai_reply)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Tip: Is 'ollama serve' running?")

if __name__ == "__main__":
    chat_bot()