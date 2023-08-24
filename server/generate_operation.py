from datetime import datetime
import subprocess
import os
import sys
sys.path.append('..')
from utils.github_helper import clone_repo, checkout_branch, commit_changes, get_diff_string
from utils.file_io_helper import collect_source_code, update_source_code
from llm.basic_model import format_source_code_str, generate_code_changes
from database.operations import write_to_db

# TODO: serve the backend public/live
TEMP_REPO_DIR="temp_repo"
DEV_BRANCH_NAME="new_branch"

def main(repo_url, prompt):
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    clone_repo(repo_url, f"{TEMP_REPO_DIR}_{current_datetime}")
    checkout_branch(DEV_BRANCH_NAME)

    source_code_dict = collect_source_code("./")

    generated_code_dict = generate_code_changes(prompt, source_code_dict)
    update_source_code(generated_code_dict)

    commit_changes("Modified based on prompt")

    # TODO: handle when branch is "master" not main
    diff_string = get_diff_string("main", DEV_BRANCH_NAME)

    write_to_db(prompt, diff_string)

    # NOTE: Navigate back to original directory and remove the temporary repo
    os.chdir("..")
    subprocess.run(f"rm -rf {TEMP_REPO_DIR}_{current_datetime}", shell=True, check=True)

    return diff_string