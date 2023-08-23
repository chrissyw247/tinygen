from fastapi import FastAPI, HTTPException, Form
# TODO: improve import logic
import sys
sys.path.append('../')
from llm.generate_diff import generate_diff

app = FastAPI()

@app.post("/generate")
async def generate(repo_url: str = Form(...), prompt: str = Form(...)):
    # Validate the GitHub URL
    # TODO: input validation move to separate helper
    if "github.com" not in repo_url:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

    print(f"/generic endpoint recieved a request with repo_url: {repo_url} + prompt: {prompt}")

    diff_string = generate_diff(repo_url, prompt)

    # TODO: actually do something with the input
    return diff_string