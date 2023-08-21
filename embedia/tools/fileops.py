import os
import shutil

from embedia.core.tool import Tool


class FileRead(Tool):

    def __init__(self):
        super().__init__(name="File Read",
                         desc="Read a file",
                         args={"file_path": "The path to the file to be read",
                               "encoding": "The encoding of the file, defaults to utf-8"})

    async def _run(self, file_path: str, encoding: str = "utf-8"):
        with open(file_path, "r", encoding=encoding) as f:
            return f.read(), 0


class FileWrite(Tool):

    def __init__(self):
        super().__init__(name="File Write",
                         desc="Write to a file, overwrites if it exists",
                         args={"file_path": "The path to the file to be written to",
                               "content": "The content to be written to the file",
                               "encoding": "The encoding of the file, defaults to utf-8"})

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "w", encoding=encoding) as f:
            return f.write(content), 0


class FileAppend(Tool):

    def __init__(self):
        super().__init__(name="File Append",
                         desc="Append to a file, create if it doesn't exist",
                         args={"file_path": "The path to the file to be appended to",
                               "content": "The content to be appended to the file",
                               "encoding": "The encoding of the file, defaults to utf-8"})

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "a", encoding=encoding) as f:
            return f.write(content), 0


class FileDelete(Tool):

    def __init__(self, human_verification=True):
        super().__init__(name="File Delete",
                         desc="Delete a file",
                         args={"file_path": "The path to the file to be deleted"})
        self.human_verification = human_verification

    async def _run(self, file_path: str):
        if self.human_verification:
            self.confirm_before_running(file_path)
        return os.remove(file_path), 0


class FileFolderMove(Tool):

    def __init__(self):
        super().__init__(name="File Folder Move",
                         desc="Move a file or a folder",
                         args={"src": "The path to the file or folder to be moved",
                               "destination": "The path to the destination"})

    async def _run(self, src: str, destination: str):
        return os.rename(src, destination), 0


class FileCopy(Tool):

    def __init__(self):
        super().__init__(name="File Copy",
                         desc="Copy a file, overwrites if destination exists",
                         args={"file_path": "The path to the file to be copied",
                               "destination": "The path to the destination"})

    async def _run(self, file_path: str, destination: str):
        return shutil.copy2(file_path, destination), 0


class FileFolderExists(Tool):

    def __init__(self):
        super().__init__(name="File Folder Exists",
                         desc="Check if a file or folder exists",
                         args={"path": "The path to the file or folder to be checked"})

    async def _run(self, path: str):
        return os.path.exists(path), 0


class FolderSearch(Tool):

    def __init__(self):
        super().__init__(name="Folder Search",
                         desc="Search for a file in a folder and its subfolders",
                         args={"folder": "The path to the folder to be searched",
                               "file_path": "The path to the file to be searched for"})

    async def _run(self, folder: str, file_path: str):
        for root, _, files in os.walk(folder):
            if file_path in files:
                return os.path.join(root, file_path), 0
        return None, 0


class FolderCreate(Tool):

    def __init__(self):
        super().__init__(name="Folder Create",
                         desc="Create a folder, ignores if it exists",
                         args={"folder": "The path to the folder to be created"})

    async def _run(self, folder: str):
        return os.makedirs(folder, exist_ok=True), 0


class FolderDelete(Tool):

    def __init__(self, human_verification=True):
        super().__init__(name="Folder Delete",
                         desc="Delete a folder and its contents, ignores if it doesn't exist",
                         args={"folder": "The path to the folder to be deleted"})
        self.human_verification = human_verification

    async def _run(self, folder: str):
        if self.human_verification:
            self.confirm_before_running(folder, contents=os.listdir(folder))
        return shutil.rmtree(folder, ignore_errors=True), 0


class FolderCopy(Tool):

    def __init__(self):
        super().__init__(name="Folder Copy",
                         desc="Copy a folder",
                         args={"folder": "The path to the folder to be copied",
                               "destination": "The path to the destination"})

    async def _run(self, folder: str, destination: str):
        if '.' in destination:
            raise NotADirectoryError("Destination must be a folder not a file")
        return shutil.copytree(folder, destination), 0


class FolderList(Tool):

    def __init__(self):
        super().__init__(name="Folder List",
                         desc="List the contents of a folder",
                         args={"folder": "The path to the folder to be listed"})

    async def _run(self, folder: str):
        return os.listdir(folder), 0
