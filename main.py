from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"mesasage": "CodeX backend in running!"}