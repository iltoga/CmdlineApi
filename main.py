import base64
import os
import subprocess
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class CommandExecutionRequest(BaseModel):
    command: str


@app.post("/execute_command/")
async def execute_command(request: CommandExecutionRequest):
    """
    Execute any Linux terminal command.
    Note: This endpoint runs on an Arch Linux distribution as a regular user.
    """
    try:
        process = subprocess.run(request.command, shell=True, capture_output=True, text=True, check=True)
        return {"output": process.stdout}
    except subprocess.CalledProcessError as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


class FileReadRequest(BaseModel):
    file_path: str


@app.get("/read_file/")
async def read_file(request: FileReadRequest):
    """
    Read a file from the Linux filesystem.
    """
    try:
        if not os.path.isfile(request.file_path):
            raise FileNotFoundError(f"File not found: {request.file_path}")

        with open(request.file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"content": content}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


class FileSaveRequest(BaseModel):
    content: str
    file_path: str
    base64_encoded: Optional[bool] = False


@app.post("/save_file/")
async def save_file(request: FileSaveRequest):
    """
    Save a file directly into the filesystem.
    If the content is base64 encoded, decode it before saving.
    """
    try:
        content = request.content
        if request.base64_encoded:
            content = base64.b64decode(content).decode("utf-8")

        os.makedirs(os.path.dirname(request.file_path), exist_ok=True)
        with open(request.file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return {"message": f"File saved successfully at {request.file_path}"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("simplified_fastapi:app", host="0.0.0.0", port=8000, reload=True)
