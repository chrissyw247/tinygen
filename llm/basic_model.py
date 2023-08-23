import subprocess
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def format_source_code_str(source_code_dict):
    source_code_str = "\n".join([f"{key}:\n{value}" for key, value in source_code_dict.items()])
    return source_code_str

def parse_source_code_str(source_code_str, filenames):
    source_code_dict = {}
    current_pos = 0

    for filename in filenames:
        # Search for the filename in the source code string
        start_pos = source_code_str.find(f"{filename}:", current_pos)
        if start_pos == -1:
            # Filename not found in the source code string
            continue

        # The filename and colon length is added to find the starting position of the content
        start_pos += len(f"{filename}:\n")

        # Find the next filename to get the ending position of the current file's content
        if filenames.index(filename) < len(filenames) - 1:
            next_filename = filenames[filenames.index(filename) + 1]
            end_pos = source_code_str.find(f"{next_filename}:", start_pos)
        else:
            end_pos = len(source_code_str)

        # Extract content and update the dictionary
        content = source_code_str[start_pos:end_pos].strip()
        source_code_dict[filename] = content

        # Update the current position for the next iteration
        current_pos = end_pos

    return source_code_dict

def generate_code_changes(prompt, source_code_dict):
    source_code_str = format_source_code_str(source_code_dict)
    filenames = list(source_code_dict.keys())

    response = openai.Edit.create(
        engine="code-davinci-edit-001",
        input=source_code_str,
        instruction=prompt,
        temperature=0,
        top_p=1
    )
    generated_code_str = response.choices[0].text.strip()
    generated_code_dict = parse_source_code_str(generated_code_str, filenames)
    print(f"GPT generated code: {json.dumps(generated_code_dict, indent=4)}")
    return generated_code_dict
