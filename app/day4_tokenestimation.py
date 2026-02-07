def analyze_prompt(text):
    """
    Day 4: Understanding Tokens & Context Windows.
    Mental Model: 1 Token ~= 0.75 words (English).
    """
    print(f"--- Analyzing Input: '{text[:40]}...' ---")
    
    # 1. Raw Stats
    word_count = len(text.split())
    char_count = len(text)
    
    # 2. Token Estimation (The Mental Model)
    # Rule of thumb: Token count is usually ~1.3 times the word count
    estimated_tokens = int(word_count * 1.3)
    
    # 3. Cost Calculation (Hypothetical API Cost)
    # Example: $0.50 per 1M input tokens
    cost_per_1m = 0.50
    estimated_cost = (estimated_tokens / 1_000_000) * cost_per_1m

    print(f"Words: {word_count}")
    print(f"Chars: {char_count}")
    print(f"Estimated Tokens: ~{estimated_tokens}")
    print(f"Hypothetical Cost (at $0.50/1M): ${estimated_cost:.6f}")
    
    # 4. Context Window Check
    # Standard Llama3 Window: 8192 Tokens
    limit = 8192
    if estimated_tokens > limit:
        print(f"⚠️ OVERFLOW: Exceeds context window of {limit} tokens!")
    else:
        print(f"✅ Safe: Uses {estimated_tokens/limit:.2%} of context window.")
    print("-" * 30)

if __name__ == "__main__":
    short_prompt = "Explain Quantum Computing in simple terms."
    long_prompt = "Here is the complete history of the Roman Empire... " * 500
    
    analyze_prompt(short_prompt)
    analyze_prompt(long_prompt)