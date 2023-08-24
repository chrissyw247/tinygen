import os

# Util checks if code is a file that contains code rather than like a config file or a generated lock file
def is_code_file(filename):
    # Check if the filename ends in a known code extension
    if filename.endswith(('.py', '.js', '.java', '.c', '.cpp', '.h', '.hpp', '.rb', '.go', '.swift', '.ts')):
       return True
    return False

def collect_source_code(repo_dir):
    source_code_dict = {}
    for root, dirs, files in os.walk(repo_dir):
        # NOTE: Skip the .git directory
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            if is_code_file(file):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                source_code_dict[file_path] = content
    return source_code_dict

def update_source_code(new_source_code_dict):
    for filename, code in new_source_code_dict.items():
        with open(filename, "w") as f:
            f.write(code)