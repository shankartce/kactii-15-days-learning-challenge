"""
Rebuild the resume database with the correct embedding model
"""
import os
import shutil
import chromadb
import ollama

DB_PATH = "./resume_db"
COLLECTION_NAME = "resume_rules"
EMBEDDING_MODEL = "nomic-embed-text"

print("🗑️  Deleting old resume database...")
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)
    print("✅ Old database deleted.")
else:
    print("⚠️  No existing database found (this is fine).")

print("\n🔨 Creating new database with nomic-embed-text...")

# Custom Embedding Function
class OllamaEF(chromadb.EmbeddingFunction):
    def __init__(self, model_name=EMBEDDING_MODEL):
        self.model_name = model_name
    
    def __call__(self, input):
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

# Create new client and collection
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=OllamaEF(),
    metadata={"hnsw:space": "cosine"}
)

print("📂 Loading best practices...")
if not os.path.exists("best_practices.txt"):
    print("❌ Error: 'best_practices.txt' not found!")
    exit(1)

with open("best_practices.txt", "r") as f:
    rules = [line.strip() for line in f if line.strip()]

print(f"📚 Indexing {len(rules)} resume rules...")
ids = [f"rule_{i}" for i in range(len(rules))]
collection.upsert(documents=rules, ids=ids)

print(f"✅ Successfully indexed {len(rules)} rules!")
print("\n📋 Rules in database:")
for i, rule in enumerate(rules, 1):
    print(f"  {i}. {rule[:80]}...")

print("\n✨ Database rebuilt successfully!")
print("You can now run: python day14_final_project.py")
