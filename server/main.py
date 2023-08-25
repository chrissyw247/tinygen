from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from . import generate_operation
import sys
sys.path.append('..')
from utils.github_helper import validate_repo_url
from utils.error_helper import raise_standard_error

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.post("/generate")
async def generate(repo_url: str = Form(...), prompt: str = Form(...)):
    print(f"/generic endpoint recieved a request with repo_url: {repo_url} + prompt: {prompt}")
    diff_string = ""
    try:
        validate_repo_url(repo_url)
        diff_string = generate_operation.main(repo_url, prompt)
    except HTTPException as he:
        raise_standard_error(he.status_code, he.detail)
    except Exception as e:
        raise_standard_error(500, str(e))

    return diff_string

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    content = """
    <html>
        <head>
            <title>TinyGen</title>
            <link rel="icon" href="assets/favicon.ico" type="image/x-icon">
        </head>
        <body>
            <div style="display: flex; justify-content: space-between; margin: 20px;">
                <div style="flex: 1; margin-right: 50px">
                    <h2 style="margin-top: 0">TinyGen</h2>
                    <p>TinyGen lets you generate code changes automagically with GPT!</p>
                    <p>To use follow these instructions:</p>
                    <ol>
                        <li>Enter the repository URL you would like to update in the "Repo URL" field</li>
                        <li>Enter what code changes you would like in the "Prompt" field.</li>
                    </ol>
                </div>
                <div style="flex: 2;" >
                    <form id="queryForm">
                        <div style="display: flex; flex-direction: column">
                            <label for="repoUrl">Repo URL:</label>
                            <input  type="text" id="repoUrl" name="repoUrl" value="https://github.com/jayhack/llm.sh"><br><br>

                            <label for="prompt">Prompt:</label>
                            <textarea rows="10" columns="50" id="prompt" name="prompt">add a check for which os type</textarea><br><br>

                            <button style="width: 40%; height: 30px; background-color: palegreen" type="button" onclick="fetchData()">Generate diff</button>
                        </div>
                    </form>

                    <div style="display: none; color: #D4A121" id="loadingIndicator">Loading...</div>

                    <pre style="color: green" id="generatedDiff"></pre>
                    <pre style="color: red" id="apiError"></pre>

                </div>
            </div>

            <script>
                async function fetchData() {
                    // NOTE: clear existing response + show loading indicator
                    document.getElementById("generatedDiff").textContent = ""
                    document.getElementById("apiError").textContent = ""
                    document.getElementById("loadingIndicator").style.display = "block";

                    const formData = new FormData();
                    formData.append("repo_url", document.getElementById("repoUrl").value)
                    formData.append("prompt", document.getElementById("prompt").value)

                    const res = await fetch("/generate", {
                        method: "POST",
                        body: formData
                    });

                    const data = await res.json();

                    // NOTE: check if the returned object contains a "detail" key, which indicates an error
                    if (data.hasOwnProperty("detail")) {
                        document.getElementById("apiError").textContent = `Error: ${data.detail}`;
                    } else {
                        document.getElementById("generatedDiff").textContent = data
                    }

                    // NOTE: clear loading indicator
                    document.getElementById("loadingIndicator").style.display = "none";
                }
            </script>
        </body>
    </html>
    """
    return content
