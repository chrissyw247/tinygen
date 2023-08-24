import subprocess
import os
import sys
sys.path.append('..')
from utils.github_helper import clone_repo, checkout_branch, get_diff_string, DEV_BRANCH_NAME, TEMP_REPO_DIR
from utils.file_io_helper import collect_source_code
from llm.basic_model import generate_validated_diff
from database.operations import write_to_db

def main(repo_url, prompt):
    # NOTE: prepare variables + workspace. clone repo to temp directory
    repo_dir = clone_repo(repo_url)
    checkout_branch(DEV_BRANCH_NAME)
    source_code_dict = collect_source_code("./")

    diff_string = generate_validated_diff(prompt, source_code_dict)

    write_to_db(prompt, diff_string)

    # NOTE: Navigate back to original directory and remove the temporary repo
    os.chdir("..")
    subprocess.run(f"rm -rf {repo_dir}", shell=True, check=True)

    return diff_string
