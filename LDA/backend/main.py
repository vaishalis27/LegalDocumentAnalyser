from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import document 

app = FastAPI(
    title="AI-Based Legal Document Analyzer",
    description="Summarize, analyze and extract key points from legal documents",
    version="1.0.0"
)

# CORS config (helpful for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 👇 include the router
app.include_router(document.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Legal Document Analyzer API is running 🚀"}
