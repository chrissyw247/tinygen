import subprocess
import os
import sys
sys.path.append('..')
from utils.github_helper import clone_repo, checkout_branch, commit_changes, get_diff_string
from llm.base_model import respond_to_prompt

TEMP_REPO_DIR="temp_repo"
DEV_BRANCH_NAME="new_branch"

def main(repo_url, prompt):
    clone_repo(repo_url, TEMP_REPO_DIR)
    checkout_branch(DEV_BRANCH_NAME)

    generated_changes = respond_to_prompt(prompt)
    # TODO: after LLM is created, write generated changes instead of these mock ones
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