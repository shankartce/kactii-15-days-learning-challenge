"""
Quick test to verify the resume reviewer setup
"""
import os
import sys

print("🔍 Checking Resume Reviewer Setup...\n")

# Check 1: Templates directory
if os.path.exists("templates"):
    print("✅ templates/ directory exists")
    if os.path.exists("templates/index.html"):
        print("✅ templates/index.html exists")
    else:
        print("❌ templates/index.html missing")
        sys.exit(1)
else:
    print("❌ templates/ directory missing")
    sys.exit(1)

# Check 2: Best practices file
if os.path.exists("best_practices.txt"):
    print("✅ best_practices.txt exists")
    with open("best_practices.txt", "r") as f:
        rules = [line.strip() for line in f if line.strip()]
    print(f"   Found {len(rules)} resume rules")
else:
    print("❌ best_practices.txt missing")
    sys.exit(1)

# Check 3: Required imports
print("\n🔍 Checking Python dependencies...")
try:
    import ollama
    print("✅ ollama installed")
except ImportError:
    print("❌ ollama not installed - run: pip install ollama")
    sys.exit(1)

try:
    import chromadb
    print("✅ chromadb installed")
except ImportError:
    print("❌ chromadb not installed - run: pip install chromadb")
    sys.exit(1)

try:
    import fastapi
    print("✅ fastapi installed")
except ImportError:
    print("❌ fastapi not installed - run: pip install fastapi")
    sys.exit(1)

try:
    import uvicorn
    print("✅ uvicorn installed")
except ImportError:
    print("❌ uvicorn not installed - run: pip install uvicorn[standard]")
    sys.exit(1)

try:
    import jinja2
    print("✅ jinja2 installed")
except ImportError:
    print("❌ jinja2 not installed - run: pip install jinja2")
    sys.exit(1)

# Check 4: Ollama models
print("\n🔍 Checking Ollama models...")
try:
    models = ollama.list()
    model_names = [m['name'] for m in models['models']]
    
    if any('llama3.2' in name for name in model_names):
        print("✅ llama3.2 model available")
    else:
        print("⚠️  llama3.2 not found - run: ollama pull llama3.2")
    
    if any('nomic-embed-text' in name for name in model_names):
        print("✅ nomic-embed-text model available")
    else:
        print("⚠️  nomic-embed-text not found - run: ollama pull nomic-embed-text")
        
except Exception as e:
    print(f"⚠️  Could not check Ollama models: {e}")
    print("   Make sure Ollama is running: ollama serve")

print("\n" + "="*50)
print("✨ Setup check complete!")
print("="*50)
print("\nTo start the application, run:")
print("  python day14_final_project.py")
print("\nThen open: http://localhost:8000")
