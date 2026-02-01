import chromadb
import ollama
from chromadb.utils import embedding_functions

# 1. Setup Database Connection
# We use the same path as Day 9 to load your existing data
client = chromadb.PersistentClient(path="./my_vectordb")

# Use a standard embedding function (or the custom one from Day 9)
# For simplicity in this demo, we redefine the custom one briefly:
class OllamaEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, model_name='nomic-embed-text'):
        self.model_name = model_name
    
    def __call__(self, input):
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

collection = client.get_collection(
    name="kactii_knowledge_base",
    embedding_function=OllamaEmbeddingFunction()
)

# Debug: Check what's actually in the database
print("🔍 Inspecting Database Contents...")
try:
    all_docs = collection.get()
    print(f"📊 Total documents in database: {len(all_docs['ids'])}")
    for i, (doc_id, doc) in enumerate(zip(all_docs['ids'], all_docs['documents']), 1):
        print(f"  [{doc_id}]: {doc}")
except Exception as e:
    print(f"⚠️  Error inspecting database: {e}")
print("-" * 60)

def rag_query(user_question):
    print(f"\n❓ User Question: '{user_question}'")
    
    # STEP 1: RETRIEVAL (The Search)
    print("🔍 Searching Knowledge Base...")
    results = collection.query(
        query_texts=[user_question],
        n_results=4 # Get all documents
    )
    
    # Check if we found anything
    if not results['documents'][0]:
        print("❌ No relevant information found.")
        return

    # Hybrid approach: Combine semantic search with keyword matching
    docs = results['documents'][0]
    distances = results['distances'][0]
    
    # Extract key terms from question (simple approach)
    question_words = set(user_question.lower().split())
    
    best_idx = 0
    best_score = float('inf')
    
    print(f"📚 Analyzing {len(docs)} documents:")
    for i, doc in enumerate(docs):
        doc_words = set(doc.lower().split())
        # Count matching keywords
        keyword_matches = len(question_words & doc_words)
        # Combine semantic distance with keyword bonus
        # Lower distance is better, so subtract keyword matches
        combined_score = distances[i] - (keyword_matches * 0.2)
        
        print(f"  [{i+1}] distance: {distances[i]:.4f}, keywords: {keyword_matches}, score: {combined_score:.4f}")
        print(f"      '{doc}'")
        
        if combined_score < best_score:
            best_score = combined_score
            best_idx = i
    
    retrieved_context = docs[best_idx]
    print(f"✅ Best Match (index {best_idx + 1}): '{retrieved_context}'")
    
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
    rag_query("What does Kactii Academy offer?")