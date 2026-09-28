from fastapi import FastAPI
from backend.routes.query import router

app = FastAPI(title="Neuro-Symbolic RAG System")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "AI System is running"}