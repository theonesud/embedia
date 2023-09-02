import os
import shutil

from embedia.core.tool import Tool
from embedia.schema.tool import ToolReturn, ArgDocumentation, ToolDocumentation


class FileRead(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="File Read",
            desc="Read a file",
            args=[ArgDocumentation(
                name="file_path",
                desc="The path to the file to be read (type: str)"
            ), ArgDocumentation(
                name="encoding",
                desc="The encoding of the file, defaults to utf-8 (type: str)"
            )]))

    async def _run(self, file_path: str, encoding: str = "utf-8"):
        with open(file_path, "r", encoding=encoding) as f:
            return ToolReturn(output=f.read(), exit_code=0)


class FileWrite(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="File Write",
            desc="Write to a file, overwrites if it exists",
            args=[ArgDocumentation(
                name="file_path",
                desc="The path to the file to be written to (type: str)"
            ), ArgDocumentation(
                name="content",
                desc="The content to be written to the file (type: str)"
            ), ArgDocumentation(
                name="encoding",
                desc="The encoding of the file, defaults to utf-8 (type: str)"
            )]))

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "w", encoding=encoding) as f:
            return ToolReturn(output=f.write(content), exit_code=0)


class FileAppend(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="File Append",
            desc="Append to a file, create if it doesn't exist",
            args=[ArgDocumentation(
                name="file_path",
                desc="The path to the file to be appended to (type: str)"
            ), ArgDocumentation(
                name="content",
                desc="The content to be appended to the file (type: str)"
            ), ArgDocumentation(
                name="encoding",
                desc="The encoding of the file, defaults to utf-8 (type: str)"
            )]))

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "a", encoding=encoding) as f:
            return ToolReturn(output=f.write(content), exit_code=0)


class FileDelete(Tool):

    def __init__(self, verify_before_deleting=True):
        super().__init__(docs=ToolDocumentation(
            name="File Delete",
            desc="Delete a file",
            args=[ArgDocumentation(
                name="file_path",
                desc="The path to the file to be deleted (type: str)"
            )]))
        self.verify_before_deleting = verify_before_deleting

    async def _run(self, file_path: str):
        if self.verify_before_deleting:
            await self.human_confirmation(file_path)
        return ToolReturn(output=os.remove(file_path), exit_code=0)


class FileFolderMove(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="File Folder Move",
            desc="Move a file or a folder",
            args=[ArgDocumentation(
                name="src",
                desc="The path to the file or folder to be moved (type: str)"
            ), ArgDocumentation(
                name="destination",
                desc="The path to the destination (type: str)"
            )]))

    async def _run(self, src: str, destination: str):
        return ToolReturn(output=os.rename(src, destination), exit_code=0)


class FileCopy(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="File Copy",
            desc="Copy a file, overwrites if destination exists",
            args=[ArgDocumentation(
                name="file_path",
                desc="The path to the file to be copied (type: str)"
            ), ArgDocumentation(
                name="destination",
                desc="The path to the destination (type: str)"
            )]))

    async def _run(self, file_path: str, destination: str):
        return ToolReturn(output=shutil.copy2(file_path, destination), exit_code=0)


class FileFolderExists(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="File Folder Exists",
            desc="Check if a file or folder exists",
            args=[ArgDocumentation(
                name="path",
                desc="The path to the file or folder to be checked (type: str)"
            )]))

    async def _run(self, path: str):
        return ToolReturn(output=os.path.exists(path), exit_code=0)


class FolderSearch(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Folder Search",
            desc="Search for a file in a folder and its subfolders",
            args=[ArgDocumentation(
                name="folder",
                desc="The path to the folder to be searched (type: str)"
            ), ArgDocumentation(
                name="file_path",
                desc="The path to the file to be searched for (type: str)"
            )]))

    async def _run(self, folder: str, file_path: str):
        for root, _, files in os.walk(folder):
            if file_path in files:
                return ToolReturn(output=os.path.join(root, file_path), exit_code=0)
        return ToolReturn(output=None, exit_code=1)


class FolderCreate(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Folder Create",
            desc="Create a folder, ignores if it exists",
            args=[ArgDocumentation(
                name="folder",
                desc="The path to the folder to be created (type: str)"
            )]))

    async def _run(self, folder: str):
        return ToolReturn(output=os.makedirs(folder, exist_ok=True), exit_code=0)


class FolderDelete(Tool):

    def __init__(self, verify_before_deleting=True):
        super().__init__(docs=ToolDocumentation(
            name="Folder Delete",
            desc="Delete a folder and its contents, ignores if it doesn't exist",
            args=[ArgDocumentation(
                name="folder",
                desc="The path to the folder to be deleted (type: str)"
            )]))

        self.verify_before_deleting = verify_before_deleting

    async def _run(self, folder: str):
        if self.verify_before_deleting:
            await self.human_confirmation({'folder_name': folder, 'contents': os.listdir(folder)})
        return ToolReturn(output=shutil.rmtree(folder, ignore_errors=True), exit_code=0)


class FolderCopy(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Folder Copy",
            desc="Copy a folder",
            args=[ArgDocumentation(
                name="folder",
                desc="The path to the folder to be copied (type: str)"
            ), ArgDocumentation(
                name="destination",
                desc="The path to the destination (type: str)"
            )]))

    async def _run(self, folder: str, destination: str):
        return ToolReturn(output=shutil.copytree(folder, destination), exit_code=0)


class FolderList(Tool):

    def __init__(self):
        super().__init__(docs=ToolDocumentation(
            name="Folder List",
            desc="List the contents of a folder",
            args=[ArgDocumentation(
                name="folder",
                desc="The path to the folder to be listed (type: str)"
            )]))

    async def _run(self, folder: str):
        return ToolReturn(output=os.listdir(folder), exit_code=0)
