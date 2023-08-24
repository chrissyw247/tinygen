from fastapi import HTTPException
import subprocess
import openai
import os
import json
import sys
sys.path.append('..')
from utils.file_io_helper import update_source_code
from utils.github_helper import commit_changes, get_diff_string, DEV_BRANCH_NAME

openai.api_key = os.getenv("OPENAI_API_KEY")

# TODO: move these format/parsing methods to separate util
def format_filename_heading(filename):
    return f"##{filename}##"

def format_source_code_str(source_code_dict):
    # TODO: add a new line at top of file?
    source_code_str = "\n".join([f"{format_filename_heading(filename)}:\n{source_code}" for filename, source_code in source_code_dict.items()])
    return source_code_str

def parse_source_code_str(source_code_str, filenames):
    source_code_dict = {}
    current_pos = 0

    for filename in filenames:
        # Search for the filename in the source code string
        start_pos = source_code_str.find(f"{format_filename_heading(filename)}:\n", current_pos)
        if start_pos == -1:
            # Filename not found in the source code string
            continue

        # The filename and colon length is added to find the starting position of the content
        start_pos += len(f"{format_filename_heading(filename)}:\n")

        # Find the next filename to get the ending position of the current file's content
        if filenames.index(filename) < len(filenames) - 1:
            next_filename = filenames[filenames.index(filename) + 1]
            end_pos = source_code_str.find(f"{format_filename_heading(next_filename)}:\n", start_pos)
        else:
            end_pos = len(source_code_str)

        # Extract content and update the dictionary
        # NOTE: Subtract 1 from the end_pos to account for \n separator
        content = source_code_str[start_pos:end_pos-1]
        source_code_dict[filename] = content

        # Update the current position for the next iteration
        current_pos = end_pos

    return source_code_dict

def generate_code_changes(prompt, source_code_dict):
    source_code_str = format_source_code_str(source_code_dict)
    response = {}

    try:
        response = openai.Edit.create(
            engine="code-davinci-edit-001",
            input=source_code_str,
            instruction=prompt,
            temperature=0,
            top_p=1
        )
    except openai.error.InvalidRequestError as e:
        raise HTTPException(status_code=400, detail="Github repo is too large :(")

    generated_code_str = response.choices[0].text
    filenames = list(source_code_dict.keys())
    generated_code_dict = parse_source_code_str(generated_code_str, filenames)
    return generated_code_dict

def generate_diff(prompt, source_code_dict):
    generated_code_dict = generate_code_changes(prompt, source_code_dict)
    update_source_code(generated_code_dict)
    commit_changes("Modified based on prompt")

    # TODO: handle when branch is "master" not main
    diff_string = get_diff_string("main", DEV_BRANCH_NAME)
    return diff_string

def generate_validated_diff(prompt, source_code_dict, num_validations=1):
    diff_string = generate_diff(prompt, source_code_dict)

    # Verify edits made by GPT
    verification_passed = verify_generated_code(prompt, source_code_dict, diff_string)

    if (verification_passed):
        print(f"Verification passed!!")
        return diff_string
    else:
        # TODO: retry generation num_validations times
        print(f"Verification failed! Returning empty diff.")
        return ""

def verify_generated_code(prompt, source_code_dict, generated_diff):
    print(f"source_code_dict: {source_code_dict}")
    print(f"generated_diff: {generated_diff}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": f"{format_source_code_str(source_code_dict)}"},
            {"role": "user", "content": f"For the prompt: {prompt} this is the diff that GPT came up with: {generated_diff}. Does this look good? Respond yes or no."},
        ],
        temperature=0,
        max_tokens=1000
    )

    assistant_message = response.choices[0].message.content
    print(f"Assistant response: {assistant_message}")
    return 'yes' in assistant_message.lower()
