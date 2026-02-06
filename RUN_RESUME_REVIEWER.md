# 🎯 AI Resume Reviewer - Quick Start Guide

## Prerequisites

1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

2. Ensure you have the required models:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Build the resume database (first time only):
   ```bash
   python rebuild_resume_db.py
   ```

## Running the Application

1. Start the server:
   ```bash
   python day14_final_project.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:8000
   ```

3. Paste your resume text and click "Review My Resume"

4. Wait a few seconds for the AI to analyze and provide feedback

## Features

- ✨ Beautiful, modern web interface
- 🤖 AI-powered resume analysis using RAG (Retrieval Augmented Generation)
- 📋 Applies best practices from your knowledge base
- 💡 Provides specific, actionable feedback
- 📊 Scores your resume out of 10
- 🔄 Suggests improved bullet points with metrics

## API Endpoint

You can also use the API programmatically:

```bash
curl -X POST http://localhost:8000/api/review \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Your resume text here..."}'
```

## Troubleshooting

- **Dimension mismatch error**: Run `python rebuild_resume_db.py` to rebuild the database
- **best_practices.txt not found**: Create it with resume writing rules
- **Port 8000 in use**: Change the port in day14_final_project.py
- **Embeddings fail**: Ensure nomic-embed-text model is pulled with `ollama pull nomic-embed-text`
