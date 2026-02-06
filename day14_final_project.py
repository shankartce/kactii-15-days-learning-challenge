import ollama
import chromadb
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os

# --- 1. CONFIGURATION ---
DB_PATH = "./resume_db"
COLLECTION_NAME = "resume_rules"
MODEL_NAME = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"

# --- 2. VECTOR DATABASE SETUP (Memory) ---
client = chromadb.PersistentClient(path=DB_PATH)

# Custom Embedding Function (using Ollama)
class OllamaEF(chromadb.EmbeddingFunction):
    def __init__(self, model_name=EMBEDDING_MODEL):
        self.model_name = model_name
    
    def __call__(self, input):
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=self.model_name, prompt=text)
            embeddings.append(response['embedding'])
        return embeddings

collection = client.get_or_create_collection(
    name=COLLECTION_NAME, 
    embedding_function=OllamaEF(),
    metadata={"hnsw:space": "cosine"}
)

# --- 3. INGESTION ENGINE (Run once on startup) ---
def ingest_knowledge_base():
    if collection.count() > 0:
        print("✅ Knowledge Base already loaded. Skipping ingestion.")
        return

    print("📂 Loading Best Practices...")
    if not os.path.exists("best_practices.txt"):
        print("❌ Error: 'best_practices.txt' not found!")
        return

    with open("best_practices.txt", "r") as f:
        rules = [line.strip() for line in f if line.strip()]

    ids = [f"rule_{i}" for i in range(len(rules))]
    collection.upsert(documents=rules, ids=ids)
    print(f"✅ Indexed {len(rules)} resume rules into Vector DB.")

# --- 4. API SERVER (FastAPI) ---
app = FastAPI(title="Resume Reviewer AI")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

class ResumeRequest(BaseModel):
    resume_text: str

@app.on_event("startup")
def startup_event():
    ingest_knowledge_base()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def review_resume_form(request: Request, resume_text: str = Form(...)):
    """Handle form submission and return results"""
    print("📥 Received Resume for Review...")
    
    if not resume_text.strip():
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please enter your resume text."
        })
    
    try:
        # Step A: RETRIEVAL (Find relevant rules based on the resume content)
        results = collection.query(
            query_texts=[resume_text[:500]],
            n_results=8
        )
        
        retrieved_rules = "\n".join(results['documents'][0])
        
        # Step B: AUGMENTATION (Inject rules into prompt)
        prompt = f"""
You are an Expert Career Coach and Resume Reviewer. Your task is to provide a detailed, actionable review of the candidate's resume based on professional best practices.

RESUME BEST PRACTICES TO APPLY:
{retrieved_rules}

CANDIDATE'S RESUME:
{resume_text}

INSTRUCTIONS:
Analyze the resume thoroughly and provide feedback in the following structured format:

1. STRENGTHS (2-3 points)
   - Identify what the candidate is doing well
   - Reference specific examples from their resume

2. CRITICAL ISSUES (3-5 points)
   - List specific problems found in the resume
   - Reference which rule number is being violated
   - Explain why each issue matters to recruiters

3. SPECIFIC IMPROVEMENTS (3-5 examples)
   - Take actual bullet points from the resume
   - Show the BEFORE version (what they wrote)
   - Show the AFTER version (improved with metrics and impact)
   - Explain what makes the improved version better

4. MISSING ELEMENTS
   - What important information is missing?
   - What should be added or expanded?

5. FORMATTING & STRUCTURE
   - Comment on layout, consistency, and readability
   - Suggest specific formatting improvements

6. OVERALL SCORE: X/10
   - Provide a numerical score with clear justification
   - Explain what would raise the score to 10/10

Be specific, direct, and actionable. Use examples from the actual resume text.
"""
        
        # Step C: GENERATION
        print("🤖 Generating Critique...")
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        feedback = response['message']['content']
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resume_text": resume_text,
            "feedback": feedback,
            "rules_applied": results['documents'][0]
        })
    
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resume_text": resume_text,
            "error": f"Error processing resume: {str(e)}"
        })

@app.post("/api/review")
def review_resume_api(request: ResumeRequest):
    """API endpoint for programmatic access"""
    print("📥 Received Resume for Review (API)...")
    
    # Step A: RETRIEVAL
    results = collection.query(
        query_texts=[request.resume_text[:500]],
        n_results=8
    )
    
    retrieved_rules = "\n".join(results['documents'][0])
    
    # Step B: AUGMENTATION
    prompt = f"""
You are an Expert Career Coach and Resume Reviewer. Your task is to provide a detailed, actionable review of the candidate's resume based on professional best practices.

RESUME BEST PRACTICES TO APPLY:
{retrieved_rules}

CANDIDATE'S RESUME:
{request.resume_text}

INSTRUCTIONS:
Analyze the resume thoroughly and provide feedback in the following structured format:

1. STRENGTHS (2-3 points)
   - Identify what the candidate is doing well
   - Reference specific examples from their resume

2. CRITICAL ISSUES (3-5 points)
   - List specific problems found in the resume
   - Reference which rule number is being violated
   - Explain why each issue matters to recruiters

3. SPECIFIC IMPROVEMENTS (3-5 examples)
   - Take actual bullet points from the resume
   - Show the BEFORE version (what they wrote)
   - Show the AFTER version (improved with metrics and impact)
   - Explain what makes the improved version better

4. MISSING ELEMENTS
   - What important information is missing?
   - What should be added or expanded?

5. FORMATTING & STRUCTURE
   - Comment on layout, consistency, and readability
   - Suggest specific formatting improvements

6. OVERALL SCORE: X/10
   - Provide a numerical score with clear justification
   - Explain what would raise the score to 10/10

Be specific, direct, and actionable. Use examples from the actual resume text.
"""
    
    # Step C: GENERATION
    print("🤖 Generating Critique...")
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    return {
        "status": "success",
        "rules_applied": results['documents'][0],
        "feedback": response['message']['content']
    }

# --- 5. RUNNER ---
if __name__ == "__main__":
    print("🚀 Starting Resume AI Server...")
    print("📍 Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)