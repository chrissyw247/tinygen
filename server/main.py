from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    content = """
    <html>
        <head>
            <title>TinyGen UI</title>
        </head>
        <body>
            <form id="queryForm">
                <label for="repoUrl">Repo URL:</label>
                <input type="text" id="repoUrl" name="repoUrl" value="https://github.com/jayhack/llm.sh"><br><br>

                <label for="prompt">Prompt:</label>
                <input type="text" id="prompt" name="prompt" value="add a check for which os type"><br><br>

                <button type="button" onclick="fetchData()">Generate diff</button>
            </form>
            <pre id="apiResult"></pre>

            <script>
                async function fetchData() {
                    const formData = new FormData();
                    formData.append("repo_url", document.getElementById("repoUrl").value)
                    formData.append("prompt", document.getElementById("prompt").value)

                    const res = await fetch("/generate", {
                        method: "POST",
                        body: formData
                    });

                    const data = await res.json();
                    document.getElementById("apiResult").textContent = data
                }
            </script>
        </body>
    </html>
    """
    return content
