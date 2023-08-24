from fastapi import FastAPI, HTTPException, Form
from . import generate_operation

app = FastAPI()

@app.post("/generate")
async def generate(repo_url: str = Form(...), prompt: str = Form(...)):
    # Validate the GitHub URL
    # TODO: input validation move to separate helper
    # TODO: wrap in try catch
    if "github.com" not in repo_url:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

    print(f"/generic endpoint recieved a request with repo_url: {repo_url} + prompt: {prompt}")

    diff_string = generate_operation.main(repo_url, prompt)

    return diff_string