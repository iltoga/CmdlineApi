import difflib
import os
import shutil
import subprocess
import zipfile


def execute_command_logic(command: str):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    return output, error


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
