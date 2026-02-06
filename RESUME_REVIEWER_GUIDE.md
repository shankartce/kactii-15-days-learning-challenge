# 🎯 AI Resume Reviewer - Complete Guide

## What's New?

Your `day14_final_project.py` has been upgraded with:

✨ **Beautiful Web Interface**
- Modern, gradient design with purple theme
- Clean, professional layout
- Responsive design (works on mobile)
- Real-time loading indicators
- Error handling with user-friendly messages

🤖 **Enhanced AI Features**
- Uses `nomic-embed-text` for better semantic search
- Retrieves top 5 relevant rules (instead of 3)
- More detailed feedback with 2-3 weaknesses
- Concrete improvement suggestions
- Rewritten bullet points with metrics
- Overall score with justification

📋 **Dual Interface**
- Web UI at `http://localhost:8000` for interactive use
- API endpoint at `http://localhost:8000/api/review` for programmatic access

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Ensure Ollama Models
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 3. Run the Application
```bash
python day14_final_project.py
```

### 4. Open Your Browser
Navigate to: `http://localhost:8000`

## How to Use

### Web Interface

1. **Paste Your Resume**: Copy your resume text into the large text area
2. **Click "Review My Resume"**: The AI will analyze your resume
3. **Wait**: Processing takes 5-15 seconds depending on resume length
4. **Review Feedback**: Read the detailed feedback below your resume
5. **See Applied Rules**: Check which best practices were used in the review

### Sample Resume

Use the content from `sample_resume.txt` to test the application. This resume intentionally has issues that the AI will catch:
- Vague bullet points without metrics
- Passive language ("Responsible for")
- Clichés ("hard worker", "team player")
- Missing quantifiable achievements

### API Usage

For programmatic access:

```bash
curl -X POST http://localhost:8000/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume content here..."
  }'
```

Response format:
```json
{
  "status": "success",
  "rules_applied": ["Rule 1", "Rule 2", ...],
  "feedback": "Detailed AI feedback..."
}
```

## Architecture

### RAG Pipeline

1. **Ingestion** (Startup)
   - Loads `best_practices.txt`
   - Creates embeddings using `nomic-embed-text`
   - Stores in ChromaDB vector database

2. **Retrieval** (Per Request)
   - Takes first 500 chars of resume
   - Finds 5 most relevant rules using cosine similarity
   - Hybrid search (semantic + keyword matching)

3. **Augmentation** (Per Request)
   - Injects retrieved rules into prompt
   - Adds resume text
   - Structures the task for the AI

4. **Generation** (Per Request)
   - Sends augmented prompt to `llama3.2`
   - Receives structured feedback
   - Returns to user

## File Structure

```
.
├── day14_final_project.py      # Main application
├── templates/
│   └── index.html              # Web interface
├── best_practices.txt          # Resume rules knowledge base
├── resume_db/                  # Vector database (auto-created)
├── sample_resume.txt           # Test resume
├── test_resume_app.py          # Setup verification
└── requirements.txt            # Python dependencies
```

## Customization

### Add More Rules

Edit `best_practices.txt` and add new lines:
```
Resume Rule #6: Include a summary section at the top highlighting key achievements.
Resume Rule #7: Use consistent formatting for dates and locations.
```

Then delete the `resume_db/` folder and restart the app to re-index.

### Change AI Model

In `day14_final_project.py`, modify:
```python
MODEL_NAME = "llama3.2"  # Change to any Ollama model
EMBEDDING_MODEL = "nomic-embed-text"  # Change embedding model
```

### Customize UI Colors

Edit `templates/index.html` and change the gradient:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adjust Feedback Detail

In the prompt section, modify the TASK instructions to get different types of feedback.

## Troubleshooting

### Port Already in Use
```bash
# Change port in day14_final_project.py
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use 8001 instead
```

### Slow Response Times
- Reduce `n_results` from 5 to 3
- Use a smaller model like `llama3.2:1b`
- Limit resume text length in the query

### Database Issues
```bash
# Delete and rebuild
rm -rf resume_db/
python day14_final_project.py
```

### Template Not Found
Make sure `templates/` directory exists in the same folder as the Python file.

## Tips for Best Results

1. **Paste Complete Sections**: Include full experience entries, not fragments
2. **Include Context**: Add job titles, companies, dates
3. **Test Iterations**: Try different versions to see improvements
4. **Use Specific Questions**: Ask about particular sections in the resume text
5. **Review Multiple Times**: Each run may catch different issues

## Next Steps

- Add file upload functionality
- Export feedback as PDF
- Compare before/after versions
- Add industry-specific rule sets
- Implement user accounts and history
- Add A/B testing for different prompts

Enjoy your AI-powered resume reviewer! 🚀
