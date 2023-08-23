import subprocess
import os

def clone_repo(repo_url, repo_dir):
    clone_command = f"git clone {repo_url} {repo_dir}"
    subprocess.run(clone_command, shell=True, check=True)
    os.chdir(repo_dir)

def checkout_branch(branch_name):
    subprocess.run(f"git checkout -b {branch_name}", shell=True, check=True)

def commit_changes(commit_message):
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run(f"git commit -m '{commit_message}'", shell=True, check=True)

def get_diff_string(src_branch, dest_branch):
    result = subprocess.run(f"git diff {src_branch}..{dest_branch}", shell=True, check=True, capture_output=True, text=True)
    diff_output = result.stdout
    return diff_output