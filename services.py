import difflib
import logging
import os
import shutil
import subprocess
import zipfile
from typing import Dict, Optional, Tuple

from fastapi import HTTPException


def execute_command_logic(command: str, working_directory: Optional[str] = None) -> Tuple[str, str]:
    """
    Execute a command and return its output and error.

    Args:
    command (str): The command to be executed.
    working_directory (Optional[str]): The directory in which to execute the command.

    Returns:
    Tuple[str, str]: The standard output and error of the command.
    """
    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=working_directory
        )
        output, error = process.communicate()

        if process.returncode != 0:
            error_info = f"Command '{command}' failed with return code {process.returncode}: {error}"
            logging.error(error_info)
            return output, error_info

        return output, error

    except subprocess.CalledProcessError as cpe:
        error_msg = f"Subprocess error: {cpe}"
        logging.error(error_msg)
        raise cpe
    except Exception as e:
        logging.error(f"Error executing command: {e}")
        raise e


def read_file_logic(file_path: str):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def upload_file_logic(file):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file.filename


def diff_files_logic(file1_path: str, file2_path: str):
    with open(file1_path, "r") as file1, open(file2_path, "r") as file2:
        diff = difflib.unified_diff(
            file1.readlines(),
            file2.readlines(),
            fromfile=file1_path,
            tofile=file2_path,
        )
    return "\n".join(diff)


def execute_git_command_logic(git_command: str):
    process = subprocess.Popen(
        git_command, shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    output, error = process.communicate()
    return output, error


def zip_files_logic(directory_path: str, output_zip_path: str):
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), os.path.join(directory_path, "..")),
                )
    return f"Directory {directory_path} zipped as {output_zip_path}"


def execute_system_command(command: str, working_dir: Optional[str] = None):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir)
        output, error = process.communicate()
        return {"output": output.decode(), "error": error.decode()}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


def execute_code(
    interpreter: str, code: Optional[str] = None, inputs: Optional[str] = None, file_path: Optional[str] = None
) -> Dict[str, str]:
    try:
        # Validate the inputs
        if not code and not file_path:
            raise ValueError("Either code or file_path must be provided")

        # Prepare the command and the process
        if code:
            # Using a list to pass arguments to avoid shell interpretation
            command = [interpreter, "-c", code]
        else:
            command = [interpreter, file_path]

        # Set up the subprocess to execute the code
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Run the code and capture output and error
        output, error = process.communicate(input=inputs)

        if process.returncode != 0:
            error_info = f"Execution failed with return code {process.returncode}: {error}"
            return {"output": output, "error": error_info}

        return {"output": output, "error": error}

    except subprocess.CalledProcessError as cpe:
        error_msg = f"Subprocess error: {cpe}"
        raise HTTPException(status_code=500, detail=error_msg) from cpe
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


def save_plain_text_file_logic(content: str, file_path: str) -> str:
    """
    Save a plaintext file to the specified path.

    Args:
    content (str): The plaintext content to be saved.
    file_path (str): The path where the file should be saved.

    Returns:
    str: The path of the saved file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return file_path
    except Exception as e:
        raise e


import base64


def save_base64_file_logic(encoded_content: str, file_path: str) -> str:
    """
    Save a base64 encoded file to the specified path.

    Args:
    encoded_content (str): The base64 encoded content to be saved.
    file_path (str): The path where the file should be saved.

    Returns:
    str: The path of the saved file.
    """
    try:
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(encoded_content))
        return file_path
    except Exception as e:
        raise e
