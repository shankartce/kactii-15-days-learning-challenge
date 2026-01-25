def estimate_tokens(text):
    """
    A simple mental model for token counting.
    Rule of Thumb: 1 Token ≈ 0.75 words (or 4 chars) in English.
    """
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    
    # Rough estimation method
    estimated_tokens_by_word = word_count * 1.3  # (1 / 0.75 ≈ 1.33)
    estimated_tokens_by_char = char_count / 4
    
    print(f"--- Text Analysis: '{text[:30]}...' ---")
    print(f"Word Count: {word_count}")
    print(f"Character Count: {char_count}")
    print(f"Estimated Tokens (Word Method): {int(estimated_tokens_by_word)}")
    print(f"Estimated Tokens (Char Method): {int(estimated_tokens_by_char)}")
    print("-" * 30)

if __name__ == "__main__":
    prompt_1 = "Hello, world!"
    prompt_2 = "Generative AI is transforming the way we build software."
    
    estimate_tokens(prompt_1)
    estimate_tokens(prompt_2)