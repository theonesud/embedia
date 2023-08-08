from embedia.tool import Tool
import os
import shutil


class FileRead(Tool):

    def __init__(self):
        super().__init__(name="File Read",
                         desc="Read a file",
                         examples="./file.txt, /usr/bin/file.txt",
                         args="file_path: str, encoding: str = 'utf-8'",
                         returns="content: str")

    async def _run(self, file_path: str, encoding: str = "utf-8"):
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()


class FileWrite(Tool):

    def __init__(self):
        super().__init__(name="File Write",
                         desc="Write to a file, overwrites if it exists",
                         examples="./file.txt, /usr/bin/file.txt",
                         args="file_path: str, content: str, encoding: str = 'utf-8'",
                         returns="None")

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)


class FileAppend(Tool):

    def __init__(self):
        super().__init__(name="File Append",
                         desc="Append to a file, create if it doesn't exist",
                         examples="./file.txt, /usr/bin/file.txt",
                         args="file_path: str, content: str, encoding: str = 'utf-8'",
                         returns="None")

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "a", encoding=encoding) as f:
            f.write(content)


class FileDelete(Tool):

    def __init__(self, human_verification=True):
        super().__init__(name="File Delete",
                         desc="Delete a file",
                         examples="./file.txt, /usr/bin/file.txt",
                         args="file_path: str",
                         returns="None")
        self.human_verification = human_verification

    async def _run(self, file_path: str):
        if self.human_verification:
            self.confirm_before_running(file_path)
        os.remove(file_path)


class FileFolderMove(Tool):

    def __init__(self):
        super().__init__(name="File Folder Move",
                         desc="Move a file or a folder",
                         examples="./file.txt, /usr/bin",
                         args="src: str, destination: str",
                         returns="None")

    async def _run(self, src: str, destination: str):
        os.rename(src, destination)


class FileCopy(Tool):

    def __init__(self):
        super().__init__(name="File Copy",
                         desc="Copy a file, overwrites if destination exists",
                         examples="./file.txt, /usr/bin/file.txt",
                         args="file_path: str, destination: str",
                         returns="None")

    async def _run(self, file_path: str, destination: str):
        shutil.copy2(file_path, destination)


class FileFolderExists(Tool):

    def __init__(self):
        super().__init__(name="File Folder Exists",
                         desc="Check if a file or folder exists",
                         examples="./file.txt, /usr/bin",
                         args="path: str",
                         returns="exists: bool")

    async def _run(self, path: str):
        return os.path.exists(path)


class FolderSearch(Tool):

    def __init__(self):
        super().__init__(name="Folder Search",
                         desc="Search for a file in a folder and its subfolders",
                         examples="./, /usr/bin, /usr/bin/file.txt",
                         args="folder: str, file_path: str",
                         returns="relative file_path: str or None")

    async def _run(self, folder: str, file_path: str):
        for root, _, files in os.walk(folder):
            if file_path in files:
                return os.path.join(root, file_path)
        return None


class FolderCreate(Tool):

    def __init__(self):
        super().__init__(name="Folder Create",
                         desc="Create a folder, ignores if it exists",
                         examples="./folder, /usr/bin/folder",
                         args="folder: str",
                         returns="None")

    async def _run(self, folder: str):
        os.makedirs(folder, exist_ok=True)


class FolderDelete(Tool):

    def __init__(self, human_verification=True):
        super().__init__(name="Folder Delete",
                         desc="Delete a folder and its contents, ignores if it doesn't exist",
                         examples="./folder, /usr/bin/folder",
                         args="folder: str",
                         returns="None")
        self.human_verification = human_verification

    async def _run(self, folder: str):
        if self.human_verification:
            self.confirm_before_running(folder, contents=os.listdir(folder))
        shutil.rmtree(folder, ignore_errors=True)


class FolderCopy(Tool):

    def __init__(self):
        super().__init__(name="Folder Copy",
                         desc="Copy a folder",
                         examples="./folder, /usr/bin/folder",
                         args="folder: str, destination: str",
                         returns="None")

    async def _run(self, folder: str, destination: str):
        if '.' in destination:
            raise NotADirectoryError("Destination must be a folder not a file")
        shutil.copytree(folder, destination)


class FolderList(Tool):

    def __init__(self):
        super().__init__(name="Folder List",
                         desc="List the contents of a folder",
                         examples="./folder, /usr/bin/folder",
                         args="folder: str",
                         returns="contents: list[str]")

    async def _run(self, folder: str):
        return os.listdir(folder)
