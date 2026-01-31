from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os
import sys

app = FastAPI()

# defines what the frontend should send
class CodeRequest(BaseModel):
    code: str

@app.get("/")
def root():
    return {"mesasage": "CodeX backend in running!"}

@app.post("/execute")
def execute_code(request: CodeRequest):
    # Create a temp python file 
    with tempfile.NamedTemporaryFile(
        suffix=".py", delete=False, mode="w"
    ) as temp_file:
        temp_file.write(request.code)
        temp_filename = temp_file.name

    try:
        # Execute the temp python file
        result = subprocess.run(
            [sys.executable, temp_filename],
            capture_output=True,
            text=True,
            timeout=2
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {
            "error": "Code execution timed out."
        }
    
    finally:
        # Clean up the temp file
        os.remove(temp_filename)