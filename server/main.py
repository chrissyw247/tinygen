from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from . import generate_operation
import sys
sys.path.append('..')
from utils.github_helper import validate_repo_url
from utils.error_helper import raise_standard_error

app = FastAPI()

@app.post("/generate")
async def generate(repo_url: str = Form(...), prompt: str = Form(...)):
    print(f"/generic endpoint recieved a request with repo_url: {repo_url} + prompt: {prompt}")
    validate_repo_url(repo_url)
    diff_string = ""
    try:
        diff_string = generate_operation.main(repo_url, prompt)
    except Exception as e:
        raise_standard_error(500, e)

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
                <div style="display: flex; flex-direction: column">
                    <label for="repoUrl">Repo URL:</label>
                    <input style="width: 500px; display: inline-block" type="text" id="repoUrl" name="repoUrl" value="https://github.com/jayhack/llm.sh"><br><br>

                    <label for="prompt">Prompt:</label>
                    <textarea style="width: 500px; display: inline-block" rows="10" columns="50" id="prompt" name="prompt">add a check for which os type</textarea><br><br>

                    <button style="width: 200px" type="button" onclick="fetchData()">Generate diff</button>
                </div>
            </form>

            <!-- Loading indicator -->
            <div style="display: none; color: #D4A121" id="loadingIndicator">Loading...</div>

            <pre style="color: green" id="generatedDiff"></pre>
            <pre style="color: red" id="apiError"></pre>

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
