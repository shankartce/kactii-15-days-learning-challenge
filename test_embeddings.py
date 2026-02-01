"""
Test script to debug embedding similarity issues
"""
import ollama
import numpy as np
from numpy.linalg import norm

def get_embedding(text):
    response = ollama.embeddings(model='nomic-embed-text', prompt=text)
    return np.array(response['embedding'])

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# Test data
questions = [
    "What does Kactii Academy offer?",
    "Tell me about Kactii Academy",
    "Kactii Academy"
]
docs = [
    "The capital of France is Paris.",
    "Python is a popular programming language for AI.",
    "The mitochondria is the powerhouse of the cell.",
    "Kactii Academy offers a 15-day GenAI challenge."
]

for question in questions:
    print(f"\nQuestion: '{question}'")
    print("Computing embeddings...")
    
    q_emb = get_embedding(question)
    doc_embs = [get_embedding(doc) for doc in docs]
    
    print("Similarity Scores (higher = more similar):")
    for i, doc in enumerate(docs):
        sim = cosine_similarity(q_emb, doc_embs[i])
        print(f"  [{i+1}] {sim:.4f} - '{doc}'")
    
    # Find best match
    best_idx = np.argmax([cosine_similarity(q_emb, d) for d in doc_embs])
    print(f"✅ Best Match: [{best_idx + 1}] '{docs[best_idx]}'")
