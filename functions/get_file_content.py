import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        # Absolute working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize full file path
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Ensure file is inside working directory
        valid_target = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it's a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file content with truncation
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            # Check if file has more content
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"

