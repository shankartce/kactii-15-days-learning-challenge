from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import uvicorn

# 1. Initialize the App
app = FastAPI(
    title="Kactii AI API",
    description="A simple API wrapper for local LLMs",
    version="1.0.0"
)

# 2. Define the Data Model (Input Schema)
# This ensures the user sends valid JSON data
class QueryRequest(BaseModel):
    prompt: str
    model: str = "llama3.2"  # Default model

# 3. Create the Endpoint (The "Door")
@app.post("/ask")
def ask_ai(request: QueryRequest):
    """
    Send a prompt to the local LLM and get a response.
    """
    print(f"📥 Received Prompt: {request.prompt}")
    
    try:
        # Call Ollama (just like Day 5)
        response = ollama.chat(model=request.model, messages=[
            {'role': 'user', 'content': request.prompt}
        ])
        
        return {
            "status": "success",
            "model_used": request.model,
            "response": response['message']['content']
        }
        
    except Exception as e:
        # Return a clean 500 error if something explodes
        raise HTTPException(status_code=500, detail=str(e))

# 4. Run the Server
if __name__ == "__main__":
    print("🚀 Starting API Server at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)