import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory, file_path))
        if not os.path.isfile(target_dir):
            raise ValueError(f'"File not found or is not a regular file: "{file_path}"')

        target_dir_valid = (
            os.path.commonpath([working_directory, target_dir]) == working_directory
        )
        if not target_dir_valid:
            raise ValueError(
                f'Cannot read "{file_path}" as it is outside the permitted working directory'
            )

        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return content

    except Exception as e:
        return f"Error: {e}"
