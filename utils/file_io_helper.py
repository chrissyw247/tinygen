import os

def collect_source_code(repo_dir):
    source_code_dict = {}
    for root, dirs, files in os.walk(repo_dir):
        # NOTE: Skip the .git directory
        if '.git' in dirs:
            dirs.remove('.git')

        for file in files:
            # NOTE: Skip .gitignore file
            if file == ".gitignore":
                continue
            print(file)
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            source_code_dict[file_path] = content
    return source_code_dict

def update_source_code(new_source_code_dict):
    for filename, code in new_source_code_dict.items():
        with open(filename, "w") as f:
            f.write(code)