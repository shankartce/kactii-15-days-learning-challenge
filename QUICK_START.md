# 🚀 Resume Reviewer - Quick Start

## Setup (One Time)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Pull Ollama models
ollama pull llama3.2
ollama pull nomic-embed-text

# 3. Build the database
python rebuild_resume_db.py
```

## Run the Application

```bash
python day14_final_project.py
```

Then open: **http://localhost:8000**

## Test It Out

1. Copy the content from `sample_resume.txt`
2. Paste it into the web interface
3. Click "Review My Resume"
4. Wait 10-20 seconds for AI analysis
5. Review the detailed feedback

## What You'll Get

✅ **Structured Feedback** in 6 sections:
1. Strengths - What's working
2. Critical Issues - Problems with rule references
3. Specific Improvements - Before/After examples
4. Missing Elements - What to add
5. Formatting & Structure - Layout feedback
6. Overall Score - Rating with justification

✅ **20 Professional Rules** covering:
- Quantification & metrics
- Action verbs & writing style
- Business impact & value
- Formatting & structure
- Technology specifics
- Leadership & growth

✅ **Actionable Examples**:
- See your actual bullet points
- Get improved versions with metrics
- Understand why changes matter

## Files Overview

- `day14_final_project.py` - Main application
- `templates/index.html` - Web interface
- `best_practices.txt` - 20 resume rules
- `sample_resume.txt` - Test resume
- `rebuild_resume_db.py` - Database builder

## Troubleshooting

**"Dimension mismatch" error:**
```bash
python rebuild_resume_db.py
```

**Port 8000 in use:**
Edit `day14_final_project.py`, change port to 8001

**Slow responses:**
Normal - AI analysis takes 10-20 seconds

**Ollama not running:**
```bash
ollama serve
```

## Documentation

- `RUN_RESUME_REVIEWER.md` - Detailed setup guide
- `RESUME_REVIEWER_GUIDE.md` - Complete documentation
- `IMPROVEMENTS_SUMMARY.md` - What was enhanced
- `EXPECTED_FEEDBACK_EXAMPLE.md` - Sample AI output

Enjoy your AI-powered resume reviewer! 🎯
