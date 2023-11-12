from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from auth import AuthMiddleware
from services import (
    diff_files_logic,
    execute_command_logic,
    execute_git_command_logic,
    read_file_logic,
    upload_file_logic,
    zip_files_logic,
)

app = FastAPI()
app.add_middleware(AuthMiddleware)


class ExecuteCommand(BaseModel):
    command: str


@app.post("/execute_command/")
async def execute_command(data: ExecuteCommand):
    """
    Execute a terminal command.
    """
    try:
        output, error = execute_command_logic(data.command)
        return {"output": output, "error": error}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


class ReadFile(BaseModel):
    file_path: str


@app.get("/read_file/")
async def read_file(data: ReadFile):
    """
    Read the content of a specified file.
    """
    try:
        content = read_file_logic(data.file_path)
        return {"content": content}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


class UploadFileReq(BaseModel):
    file: UploadFile = File(...)


@app.post("/upload_file/")
async def upload_file(data: UploadFileReq):
    """
    Upload a file to the server.
    """
    try:
        filename = upload_file_logic(data.file)
        return {"filename": filename}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


class DiffFiles(BaseModel):
    file1_path: str
    file2_path: str


@app.post("/diff_files/")
async def diff_files(data: DiffFiles):
    """
    Diff two files and return the differences.
    """
    try:
        diff = diff_files_logic(data.file1_path, data.file2_path)
        return {"diff": diff}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


class ExecuteGitCommand(BaseModel):
    git_command: str


@app.post("/execute_git_command/")
async def execute_git_command(data: ExecuteGitCommand):
    """
    Execute a Git command.
    """
    try:
        output, error = execute_git_command_logic(data.git_command)
        return {"output": output, "error": error}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


class ZipFiles(BaseModel):
    directory_path: str
    output_zip_path: str


@app.post("/zip_files/")
async def zip_files(data: ZipFiles):
    """
    Zip files and directories.
    """
    try:
        message = zip_files_logic(data.directory_path, data.output_zip_path)
        return {"message": message}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
