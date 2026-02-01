"""
Quick script to rebuild the vector database.
Run this if you're getting incorrect search results.
"""
import chromadb
import ollama
from chromadb import Documents, EmbeddingFunction, Embeddings

# Same embedding function as day9
class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name='nomic-embed-text'):
        self.model_name = model_name
    
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

print("🗑️  Deleting old database...")
client = chromadb.PersistentClient(path="./my_vectordb")

# Delete the old collection
try:
    client.delete_collection(name="kactii_knowledge_base")
    print("✅ Old collection deleted.")
except:
    print("⚠️  No existing collection found (this is fine).")

# Recreate with fresh data
print("🔨 Creating new collection...")
collection = client.get_or_create_collection(
    name="kactii_knowledge_base",
    embedding_function=OllamaEmbeddingFunction(),
    metadata={"hnsw:space": "cosine"}  # Use cosine similarity instead of L2
)

# Add documents
print("📚 Indexing documents...")
documents = [
    "The capital of France is Paris.",
    "Python is a popular programming language for AI.",
    "The mitochondria is the powerhouse of the cell.",
    "Kactii Academy offers a 15-day GenAI challenge."
]
ids = ["doc1", "doc2", "doc3", "doc4"]

collection.upsert(documents=documents, ids=ids)
print(f"✅ Successfully indexed {len(documents)} documents!")
print("\n📋 Documents in database:")
for i, doc in enumerate(documents, 1):
    print(f"  {i}. {doc}")

print("\n✨ Database rebuilt! You can now run day10_rag.py")
