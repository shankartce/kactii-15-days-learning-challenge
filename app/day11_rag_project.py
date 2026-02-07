import chromadb
import ollama
import os

# --- Configuration ---
DB_PATH = "./my_vectordb"
COLLECTION_NAME = "personal_knowledge"
MODEL_NAME = "llama3.2"

# --- 1. Embedding Wrapper ---
class OllamaEF(chromadb.EmbeddingFunction):
    def __call__(self, input):
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=MODEL_NAME, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

# --- 2. The Ingestion Engine (Reading & Chunking) ---
def ingest_file(file_path, collection):
    print(f"📂 Reading file: {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Simple Chunking: Split by paragraphs (double newlines)
    # In production, we would use smarter splitters (e.g., overlapping windows)
    chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
    
    print(f"🧩 Split into {len(chunks)} chunks. Indexing...")
    
    # Create unique IDs for each chunk
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    # Upsert (Update or Insert) into Chroma
    collection.upsert(documents=chunks, ids=ids)
    print("✅ Indexing Complete!")

# --- 3. The Chat Loop (RAG) ---
def start_chat(collection):
    print("\n💬 System Ready. Ask questions about your document (or type 'exit').")
    
    while True:
        query = input("\nYou: ")
        if query.lower() in ['exit', 'quit']:
            break
            
        # Retrieval
        results = collection.query(query_texts=[query], n_results=1)
        
        if not results['documents'][0]:
            print("🤖 AI: I don't have enough info on that.")
            continue
            
        context = results['documents'][0][0]
        
        # Generation
        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        response = ollama.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}])
        
        print(f"🤖 AI: {response['message']['content']}")

# --- Main Execution ---
if __name__ == "__main__":
    # Setup DB
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, 
        embedding_function=OllamaEF()
    )
    
    # Check if we need to ingest data
    if os.path.exists("my_notes.txt"):
        user_choice = input("Found 'my_notes.txt'. Index it? (y/n): ")
        if user_choice.lower() == 'y':
            ingest_file("my_notes.txt", collection)
    
    start_chat(collection)