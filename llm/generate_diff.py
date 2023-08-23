import subprocess
import os
import sys
sys.path.append('../')
from utils.github_helper import clone_repo, checkout_branch, commit_changes, get_diff_string

TEMP_REPO_DIR="temp_repo"
DEV_BRANCH_NAME="new_branch"

# TODO: move this to server instead, save this file for LLM logic
def generate_diff(repo_url, prompt):
    clone_repo(repo_url, TEMP_REPO_DIR)
    checkout_branch(DEV_BRANCH_NAME)

    # Step 3: Modify the code based on the prompt (This is a placeholder)
    # Here, you would typically analyze the 'prompt' and make code changes accordingly.
    # For demonstration, let's just append the prompt to the README.md file
    # TODO: use actual LLM
    with open("README.md", "a") as f:
        f.write("\n")
        f.write(prompt)

    commit_changes("Modified based on prompt")

    # TODO: handle when branch is "master" not main
    diff_string = get_diff_string("main", DEV_BRANCH_NAME)

    # NOTE: Navigate back to original directory and remove the temporary repo
    os.chdir("..")
    subprocess.run(f"rm -rf {TEMP_REPO_DIR}", shell=True, check=True)

    return diff_string
