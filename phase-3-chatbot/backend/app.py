from main import app

# This file serves as the entry point for Hugging Face Spaces
# The FastAPI app is imported from main.py and exposed as 'app'
# Hugging Face Spaces will automatically run this when deploying

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)