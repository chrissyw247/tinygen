from datetime import datetime
import subprocess
import os
import sys
sys.path.append('..')
from utils.github_helper import clone_repo, checkout_branch, commit_changes, get_diff_string
from llm.basic_model import generate_code_changes

# TODO: serve the backend public/live
TEMP_REPO_DIR="temp_repo"
DEV_BRANCH_NAME="new_branch"
# TODO: make it work for multiple files
SOURCE_CODE="inputs/main.py"

def main(repo_url, prompt):
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    clone_repo(repo_url, f"{TEMP_REPO_DIR}_{current_datetime}")
    checkout_branch(DEV_BRANCH_NAME)
    with open(SOURCE_CODE, 'r') as f:
        source_code = f.read()

    generated_code = generate_code_changes(prompt, source_code)
    with open(SOURCE_CODE, "w") as f:
        f.write(generated_code)

    commit_changes("Modified based on prompt")

    # TODO: handle when branch is "master" not main
    diff_string = get_diff_string("main", DEV_BRANCH_NAME)

    # NOTE: Navigate back to original directory and remove the temporary repo
    os.chdir("..")
    subprocess.run(f"rm -rf {TEMP_REPO_DIR}", shell=True, check=True)

    return diff_string