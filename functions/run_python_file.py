import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory, file_path))

        if not os.path.isfile(target_file):
            raise ValueError(f'"{file_path}" does not exist or is not a regular file')

        target_file_valid = (
            os.path.commonpath([working_directory, target_file]) == working_directory
        )
        if not target_file_valid:
            raise ValueError(
                f'Cannot execute "{file_path}" as it is outside the permitted working directory'
            )

        if not file_path.endswith(".py"):
            raise ValueError(f'"{file_path}" is not a Python file')

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )

        output_string = ""
        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}"

        if not result.stdout and not result.stderr:
            output_string += "No output produced"

        if result.stdout:
            output_string += f"STDOUT: {result.stdout}"

        if result.stderr:
            output_string += f"STDERR: {result.stderr}"

        return output_string
    except Exception as e:
        return str(e)
