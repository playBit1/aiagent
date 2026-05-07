import os


def get_files_info(working_directory, directory="."):
    try:
        working_directory = os.path.abspath(working_directory)
        directory_name = f"'{directory}'" if directory != "." else "current directory"
        target_dir = os.path.normpath(os.path.join(working_directory, directory))
        if not os.path.isdir(target_dir):
            raise ValueError(f'"{directory}" is not a directory')

        target_dir_valid = (
            os.path.commonpath([working_directory, target_dir]) == working_directory
        )
        if not target_dir_valid:
            raise ValueError(
                f'Cannot list "{directory}" as it is outside the permitted working directory'
            )

        files = os.listdir(target_dir)

        return f"Result for {directory_name}:\n{'\n'.join(f' - {file}: file_size={os.path.getsize(os.path.join(target_dir, file))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, file))}' for file in files)}"
    except Exception as e:
        return f"Result for {directory_name}\n  Error: {e}"
