import chromadb
import ollama
from chromadb import Documents, EmbeddingFunction, Embeddings

# 1. Custom Embedding Function (Connecting Chroma to Ollama)
class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name='nomic-embed-text'):
        self.model_name = model_name
    
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            # Call the local model for each document
            response = ollama.embeddings(model=self.model_name, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

def run_db_experiment():
    print("--- 🗄️ Day 9: Vector Database Construction ---")
    
    # 2. Initialize Persistent Client (Saves to disk)
    # This creates a folder 'my_vectordb' in your project
    client = chromadb.PersistentClient(path="./my_vectordb")
    
    # 3. Create/Get Collection (Like a SQL Table)
    collection = client.get_or_create_collection(
        name="kactii_knowledge_base",
        embedding_function=OllamaEmbeddingFunction() # Use our local Llama3
    )
    
    # 4. Add Documents (The "Indexing" Phase)
    print("Indexing documents...")
    documents = [
        "The capital of France is Paris.",
        "Python is a popular programming language for AI.",
        "The mitochondria is the powerhouse of the cell.",
        "Kactii Academy offers a 15-day GenAI challenge."
    ]
    ids = ["doc1", "doc2", "doc3", "doc4"]
    
    collection.upsert(documents=documents, ids=ids)
    print(f"✅ Indexed {len(documents)} documents into Vector DB.")
    
    # 5. The Search (The "Retrieval" Phase)
    query = "Tell me about coding."
    print(f"\n🔍 Querying: '{query}'")
    
    results = collection.query(
        query_texts=[query],
        n_results=1 # Give me the single best match
    )
    
    # 6. Display Result
    best_match = results['documents'][0][0]
    print(f"🎯 Best Match Found: '{best_match}'")

if __name__ == "__main__":
    run_db_experiment()