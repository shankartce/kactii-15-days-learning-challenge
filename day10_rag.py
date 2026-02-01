import chromadb
import ollama
from chromadb.utils import embedding_functions

# 1. Setup Database Connection
# We use the same path as Day 9 to load your existing data
client = chromadb.PersistentClient(path="./my_vectordb")

# Use a standard embedding function (or the custom one from Day 9)
# For simplicity in this demo, we redefine the custom one briefly:
class OllamaEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input):
        embeddings = []
        for text in input:
            response = ollama.embeddings(model='llama3.2', prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

collection = client.get_collection(
    name="kactii_knowledge_base",
    embedding_function=OllamaEmbeddingFunction()
)

def rag_query(user_question):
    print(f"\n❓ User Question: '{user_question}'")
    
    # STEP 1: RETRIEVAL (The Search)
    print("🔍 Searching Knowledge Base...")
    results = collection.query(
        query_texts=[user_question],
        n_results=1 # Fetch top 1 relevant doc
    )
    
    # Check if we found anything
    if not results['documents'][0]:
        print("❌ No relevant information found.")
        return

    retrieved_context = results['documents'][0][0]
    print(f"✅ Context Found: '{retrieved_context}'")
    
    # STEP 2: AUGMENTATION (The Prompt Injection)
    # We force the AI to use OUR data, not its training data.
    rag_prompt = f"""
    You are an assistant. Answer the question ONLY using the context below.
    
    CONTEXT:
    {retrieved_context}
    
    QUESTION:
    {user_question}
    """
    
    # STEP 3: GENERATION (The Answer)
    print("🤖 Generating Answer...")
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': rag_prompt}
    ])
    
    print(f"\n💡 AI Answer:\n{response['message']['content']}")

if __name__ == "__main__":
    # Test with a question that requires the specific document from Day 9
    rag_query("Which is the capital of France?")