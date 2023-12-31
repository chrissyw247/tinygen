from datetime import datetime
import requests
import subprocess
import os
from utils.error_helper import raise_standard_error

TEMP_REPO_DIR="temp_repo"
DEV_BRANCH_NAME="new_branch"

def validate_repo_url(repo_url):
    if "github.com" not in repo_url:
        raise_standard_error(400, f"Invalid repo URL: {repo_url}")

    parts = repo_url.split("/")
    if len(parts) < 5:
        raise_standard_error(400, f"Incomplete repo URL: {repo_url}")

    owner, repo = parts[-2], parts[-1]

    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}")

    if response.status_code == 200:
        print(f"The repo: {repo_url} exists and is public.")
    elif response.status_code == 404:
        raise_standard_error(400, f"Repo: {repo_url} does not exist or is not public.")
    else:
        raise_standard_error(500, f"An error occurred while validating repo: {repo_url}.")

def clone_repo(repo_url, repo_dir=None):
    if not repo_dir:
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        repo_dir = f"{TEMP_REPO_DIR}_{current_datetime}"

    clone_command = f"git clone {repo_url} {repo_dir}"
    subprocess.run(clone_command, shell=True, check=True)
    os.chdir(repo_dir)
    return repo_dir

def checkout_branch(branch_name=None):
    if not branch_name:
        branch_name = DEV_BRANCH_NAME

    subprocess.run(f"git checkout -b {branch_name}", shell=True, check=True)

def commit_changes(commit_message):
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run(f"git commit -m '{commit_message}'", shell=True, check=False)

def get_diff_string(src_branch, dest_branch):
    result = subprocess.run(f"git diff --ignore-all-space {src_branch}..{dest_branch}", shell=True, check=True, capture_output=True, text=True)
    diff_output = result.stdout
    return diff_output
