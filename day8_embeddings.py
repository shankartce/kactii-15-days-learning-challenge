import ollama
import numpy as np
from numpy.linalg import norm

def get_embedding(text):
    """
    Calls the local Ollama model to convert text -> vector.
    """
    response = ollama.embeddings(model='llama3.2', prompt=text)
    return response['embedding']

def calculate_similarity(vec_a, vec_b):
    """
    Cosine Similarity: The higher the score (closer to 1.0), the more similar the meaning.
    Formula: (A . B) / (||A|| * ||B||)
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (norm(a) * norm(b))

def run_experiment():
    print("--- 🧠 Day 8: Semantic Search Experiment ---")
    
    # 1. The Dataset
    word_1 = "King"
    word_2 = "Queen"
    word_3 = "Apple"
    
    print(f"Generating embeddings for: {word_1}, {word_2}, {word_3}...")
    
    # 2. Convert Text to Vectors
    vec_1 = get_embedding(word_1)
    vec_2 = get_embedding(word_2)
    vec_3 = get_embedding(word_3)
    
    print(f"Vector Dimensions: {len(vec_1)} numbers representing '{word_1}'")
    
    # 3. Calculate "Meaning" Distance
    sim_1_2 = calculate_similarity(vec_1, vec_2) # King vs Queen
    sim_1_3 = calculate_similarity(vec_1, vec_3) # King vs Apple
    
    print("\n--- Results (Cosine Similarity) ---")
    print(f"Similarity ({word_1} <-> {word_2}): {sim_1_2:.4f} (High = Related)")
    print(f"Similarity ({word_1} <-> {word_3}): {sim_1_3:.4f} (Low = Unrelated)")
    
    if sim_1_2 > sim_1_3:
        print("\n✅ SUCCESS: AI understands that a King is more like a Queen than an Apple.")
    else:
        print("\n❌ FAILURE: Something is wrong with the embeddings.")

if __name__ == "__main__":
    run_experiment()