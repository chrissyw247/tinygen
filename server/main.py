from fastapi import FastAPI, HTTPException, Form

app = FastAPI()

@app.post("/generate")
async def generate(repoUrl: str = Form(...), prompt: str = Form(...)):
    # Validate the GitHub URL
    # TODO: input validation move to separate helper
    if "github.com" not in repoUrl:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

    print(f"/generic endpoint recieved a request with repoURL: {repoUrl} + prompt: {prompt}")

    # TODO: actually do something with the input
    return {"message": f"Successfully received: Repo URL is {repoUrl} and prompt is {prompt}"}