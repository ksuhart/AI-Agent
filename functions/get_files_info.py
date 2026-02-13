import os

def get_files_info(working_directory, directory="."):
    try:
        # Absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize the target directory path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Ensure target_dir is inside working_directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure target_dir is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Build output lines
        lines = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
            lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"


