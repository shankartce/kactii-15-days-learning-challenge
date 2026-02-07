import ollama
import json
import datetime
import sys

# --- 1. The Tool Registry (The "Hands") ---
def get_time(args=None):
    """Returns the current real-time including Day Name."""
    # FIXED: Added %A (Day Name) so the AI doesn't have to guess
    return datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")

def calculate(expression):
    """Safe evaluation of math expressions."""
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in str(expression)):
        return "Error: Unsafe characters."
    try:
        return str(eval(expression)) 
    except:
        return "Error: Invalid math."

TOOL_REGISTRY = {
    "get_time": get_time,
    "calculate": calculate
}

# --- 2. The System Kernel (The "Brain") ---
# FIXED: Made instructions stricter about "current" information
SYSTEM_PROMPT = """
You are an autonomous AI Agent. 

RULES:
1. If the user asks for the DATE, TIME, DAY, or "NOW", you MUST use the "get_time" tool. Do NOT guess.
2. If the user asks for MATH, use the "calculate" tool.
3. For general chat ("hello"), use "tool": "none".

AVAILABLE TOOLS:
1. "get_time": Returns current date/time. No args.
2. "calculate": Evaluates math. Args: expression (e.g. "55 * 4").

RESPONSE FORMAT (JSON ONLY):
{
  "thought": "Reasoning here...",
  "tool": "tool_name_or_none",
  "args": "arguments_or_none",
  "response": "Response if no tool needed"
}
"""

def run_agent_turn(user_input):
    try:
        print("🤔 Thinking...", end="\r")
        response = ollama.chat(
            model='llama3.2', 
            format='json',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_input}
            ]
        )
        
        decision = json.loads(response['message']['content'])
        tool_name = decision.get('tool')
        
        # --- TOOL EXECUTION BLOCK ---
        if tool_name in TOOL_REGISTRY:
            print(f"🧠 Thought: {decision.get('thought')}")
            print(f"⚙️ Action: Calling '{tool_name}'...")
            
            # Execute Tool
            func = TOOL_REGISTRY[tool_name]
            observation = func(decision.get('args'))
            print(f"🔍 Observation: {observation}")
            
            # Synthesis
            final_prompt = f"FACT: The tool returned '{observation}'. Answer the user's question: '{user_input}' based on this fact."
            
            final_response = ollama.chat(model='llama3.2', messages=[
                {'role': 'system', 'content': "You are a helpful assistant. State the facts clearly."},
                {'role': 'user', 'content': final_prompt}
            ])
            print(f"🤖 Agent: {final_response['message']['content']}\n")

        elif tool_name == "none":
            print(f"🤖 Agent: {decision.get('response')}\n")
        
        else:
            print(f"❌ Error: Unknown tool '{tool_name}'\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    print("--- My Autonomous Agent (Tools: Math, Time) ---")
    while True:
        user_text = input("👤 You: ")
        if user_text.lower() in ["exit", "quit"]: break
        run_agent_turn(user_text)