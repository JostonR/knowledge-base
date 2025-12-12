from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Knowledge Base API is running!"}
