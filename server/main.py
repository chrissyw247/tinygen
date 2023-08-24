from fastapi import FastAPI, Form
from . import generate_operation
import sys
sys.path.append('..')
from utils.github_helper import validate_repo_url

app = FastAPI()

@app.post("/generate")
async def generate(repo_url: str = Form(...), prompt: str = Form(...)):
    validate_repo_url(repo_url)

    print(f"/generic endpoint recieved a request with repo_url: {repo_url} + prompt: {prompt}")

    # TODO: wrap in try catch
    diff_string = generate_operation.main(repo_url, prompt)

    return diff_string
