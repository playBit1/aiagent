import os


def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory, file_path))

        if os.path.isdir(target_file):
            raise ValueError(f'Cannot write to "{file_path}" as it is a directory')

        target_file_valid = (
            os.path.commonpath([working_directory, target_file]) == working_directory
        )
        if not target_file_valid:
            raise ValueError(
                f'Cannot write to "{file_path}" as it is outside the permitted working directory'
            )

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
