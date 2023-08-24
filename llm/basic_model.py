from fastapi import HTTPException
import subprocess
import openai
import os
import json

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

def generate_code_changes(prompt, source_code_str):
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
    return generated_code_str

def generate_validated_code_changes(prompt, source_code_dict, num_validations=1):
    # Build source code string (to pass to GPT) from dictionary of files to their contents
    source_code_str = format_source_code_str(source_code_dict)
    generated_code_str = generate_code_changes(prompt, source_code_str)

    # Verify edits made by GPT
    verify_generated_code(prompt, source_code_str, generated_code_str)

    # TODO: actually act on verification response
    # Parse generated code dictionary from generated code string (returned by GPT)
    filenames = list(source_code_dict.keys())
    generated_code_dict = parse_source_code_str(generated_code_str, filenames)
    return generated_code_dict

def verify_generated_code(prompt, source_code_str, generated_code_str):
    print(f"source_code_str: {source_code_str}")
    print(f"generated_code_str: {generated_code_str}")

    # TODO: actually call GPT to verity
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages = [
    #         {"role": "system", "content": f"{source_code_str}"},
    #         {"role": "user", "content": f"${prompt}"},
    #     ]
    #     temperature=0,
    #     max_tokens=1000
    # )
