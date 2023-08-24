def format_filename_heading(filename):
    return f"##{filename}##"

def format_source_code_str(source_code_dict):
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
