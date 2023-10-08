import os
import shutil

from embedia.core.tool import Tool
from embedia.schema.tool import ParamDocumentation, ToolDocumentation, ToolReturn


class FileReadTool(Tool):
    """Reads a file and returns its contents.

    Parameters
    ----------
    - `file_path` (str): The path to the file to be read.
    - `encoding` (str, optional): The encoding of the file, defaults to utf-8.

    Returns
    -------
    - `output` (str): The contents of the file.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="File Read",
                desc="Reads a file and returns its contents.",
                params=[
                    ParamDocumentation(
                        name="file_path",
                        desc="The path to the file to be read (type: str)",
                    ),
                    ParamDocumentation(
                        name="encoding",
                        desc="The encoding of the file, defaults to utf-8 (type: str)",
                    ),
                ],
            )
        )

    async def _run(self, file_path: str, encoding: str = "utf-8"):
        with open(file_path, encoding=encoding) as f:
            return ToolReturn(output=f.read(), exit_code=0)


class FileWriteTool(Tool):
    """Writes the provided contents to a file, overwrites if it.

    Parameters
    ----------
    - `file_path` (str): The path to the file to be written to.
    - `content` (str): The content to be written to the file.
    - `encoding` (str, optional): The encoding of the file, defaults to utf-8.

    Returns
    -------
    - `output` (int): The number of characters written to the file.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="File Write",
                desc="Writes the provided contents to a file, overwrites if it.",
                params=[
                    ParamDocumentation(
                        name="file_path",
                        desc="The path to the file to be written to (type: str)",
                    ),
                    ParamDocumentation(
                        name="content",
                        desc="The content to be written to the file (type: str)",
                    ),
                    ParamDocumentation(
                        name="encoding",
                        desc="The encoding of the file, defaults to utf-8 (type: str)",
                    ),
                ],
            )
        )

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "w", encoding=encoding) as f:
            return ToolReturn(output=f.write(content), exit_code=0)


class FileAppendTool(Tool):
    """Appends the provided contents to a file, creates if it doesn't exist.

    Parameters
    ----------
    - `file_path` (str): The path to the file to be appended to.
    - `content` (str): The content to be appended to the file.
    - `encoding` (str, optional): The encoding of the file, defaults to utf-8.

    Returns
    -------
    - `output` (int): The number of characters written to the file.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="File Append",
                desc="Appends the provided contents to a file, creates if it doesn't exist.",
                params=[
                    ParamDocumentation(
                        name="file_path",
                        desc="The path to the file to be appended to (type: str)",
                    ),
                    ParamDocumentation(
                        name="content",
                        desc="The content to be appended to the file (type: str)",
                    ),
                    ParamDocumentation(
                        name="encoding",
                        desc="The encoding of the file, defaults to utf-8 (type: str)",
                    ),
                ],
            )
        )

    async def _run(self, file_path: str, content: str, encoding: str = "utf-8"):
        with open(file_path, "a", encoding=encoding) as f:
            return ToolReturn(output=f.write(content), exit_code=0)


class FileDeleteTool(Tool):
    """Deletes the requested file. Asks for confirmation before deleting.

    Parameters
    ----------
    - `file_path` (str): The path to the file to be deleted.

    Returns
    -------
    - `output` (None): None.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self, verify_before_deleting=True):
        super().__init__(
            docs=ToolDocumentation(
                name="File Delete",
                desc="Deletes the requested file. Asks for confirmation before deleting.",
                params=[
                    ParamDocumentation(
                        name="file_path",
                        desc="The path to the file to be deleted (type: str)",
                    )
                ],
            )
        )
        self.verify_before_deleting = verify_before_deleting

    async def _run(self, file_path: str):
        if self.verify_before_deleting:
            await self.human_confirmation(file_path)
        return ToolReturn(output=os.remove(file_path), exit_code=0)


class FileFolderMoveTool(Tool):
    """Moves a file or a folder from one location to another.
    Can also be used to rename a file or folder.

    Parameters
    ----------
    - `src` (str): The path to the file or folder to be moved.
    - `destination` (str): The path to the destination.

    Returns
    -------
    - `output` (None): None.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="File Folder Move",
                desc="Moves a file or a folder from one location to another. Can also be used to rename a file or folder.",
                params=[
                    ParamDocumentation(
                        name="src",
                        desc="The path to the file or folder to be moved (type: str)",
                    ),
                    ParamDocumentation(
                        name="destination",
                        desc="The path to the destination (type: str)",
                    ),
                ],
            )
        )

    async def _run(self, src: str, destination: str):
        return ToolReturn(output=os.rename(src, destination), exit_code=0)


class FileCopyTool(Tool):
    """Copies a file from one location to another, overwrites if destination exists.

    Parameters
    ----------
    - `file_path` (str): The path to the file to be copied.
    - `destination` (str): The path to the destination.

    Returns
    -------
    - `output` (None): None.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="File Copy",
                desc="Copies a file from one location to another, overwrites if destination exists.",
                params=[
                    ParamDocumentation(
                        name="file_path",
                        desc="The path to the file to be copied (type: str)",
                    ),
                    ParamDocumentation(
                        name="destination",
                        desc="The path to the destination (type: str)",
                    ),
                ],
            )
        )

    async def _run(self, file_path: str, destination: str):
        return ToolReturn(output=shutil.copy2(file_path, destination), exit_code=0)


class FileFolderExistsTool(Tool):
    """Check if a file or folder exists.

    Parameters
    ----------
    - `path` (str): The path to the file or folder to be checked.

    Returns
    -------
    - `output` (bool): True if exists, False if not.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="File Folder Exists",
                desc="Check if a file or folder exists.",
                params=[
                    ParamDocumentation(
                        name="path",
                        desc="The path to the file or folder to be checked (type: str)",
                    )
                ],
            )
        )

    async def _run(self, path: str):
        return ToolReturn(output=os.path.exists(path), exit_code=0)


class FolderSearchTool(Tool):
    """Searches for the location of a requested file in a folder and its subfolders.

    Parameters
    ----------
    - `folder` (str): The path to the folder to be searched.
    - `filename` (str): The name of the file to be searched for.

    Returns
    -------
    - `output` (str): The path to the file if found, None if not found.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="Folder Search",
                desc="Searches for the location of a requested file in a folder and its subfolders.",
                params=[
                    ParamDocumentation(
                        name="folder",
                        desc="The path to the folder to be searched (type: str)",
                    ),
                    ParamDocumentation(
                        name="filename",
                        desc="The name of the file to be searched for (type: str)",
                    ),
                ],
            )
        )

    async def _run(self, folder: str, filename: str):
        for root, _, files in os.walk(folder):
            if filename in files:
                return ToolReturn(output=os.path.join(root, filename), exit_code=0)
        return ToolReturn(output=None, exit_code=1)


class FolderCreateTool(Tool):
    """Creates a folder, ignores if it exists.

    Parameters
    ----------
    - `folder` (str): The path to the folder to be created.

    Returns
    -------
    - `output` (None): None.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="Folder Create",
                desc="Creates a folder, ignores if it exists.",
                params=[
                    ParamDocumentation(
                        name="folder",
                        desc="The path to the folder to be created (type: str)",
                    )
                ],
            )
        )

    async def _run(self, folder: str):
        return ToolReturn(output=os.makedirs(folder, exist_ok=True), exit_code=0)


class FolderDeleteTool(Tool):
    """Deletes the requested folder and its contents, ignores if it doesn't exist.
    Asks for confirmation before deleting.

    Parameters
    ----------
    - `folder` (str): The path to the folder to be deleted.

    Returns
    -------
    - `output` (None): None.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self, verify_before_deleting=True):
        super().__init__(
            docs=ToolDocumentation(
                name="Folder Delete",
                desc="Deletes the requested folder and its contents, ignores if it doesn't exist. Asks for confirmation before deleting.",
                params=[
                    ParamDocumentation(
                        name="folder",
                        desc="The path to the folder to be deleted (type: str)",
                    )
                ],
            )
        )

        self.verify_before_deleting = verify_before_deleting

    async def _run(self, folder: str):
        if self.verify_before_deleting:
            await self.human_confirmation(
                {"folder_name": folder, "contents": os.listdir(folder)}
            )
        return ToolReturn(output=shutil.rmtree(folder, ignore_errors=True), exit_code=0)


class FolderCopyTool(Tool):
    """Copies a folder from one location to another.

    Parameters
    ----------
    - `folder` (str): The path to the folder to be copied.
    - `destination` (str): The path to the destination.

    Returns
    -------
    - `output` (None): None.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="Folder Copy",
                desc="Copies a folder from one location to another.",
                params=[
                    ParamDocumentation(
                        name="folder",
                        desc="The path to the folder to be copied (type: str)",
                    ),
                    ParamDocumentation(
                        name="destination",
                        desc="The path to the destination (type: str)",
                    ),
                ],
            )
        )

    async def _run(self, folder: str, destination: str):
        return ToolReturn(output=shutil.copytree(folder, destination), exit_code=0)


class FolderListTool(Tool):
    """Lists the contents of the requested folder.

    Parameters
    ----------
    - `folder` (str): The path to the folder to be listed.

    Returns
    -------
    - `output` (List[str]): The contents of the folder.
    - `exit_code` (int): 0 if success, 1 if failure.
    """

    def __init__(self):
        super().__init__(
            docs=ToolDocumentation(
                name="Folder List",
                desc="Lists the contents of the requested folder.",
                params=[
                    ParamDocumentation(
                        name="folder",
                        desc="The path to the folder to be listed (type: str)",
                    )
                ],
            )
        )

    async def _run(self, folder: str):
        return ToolReturn(output=os.listdir(folder), exit_code=0)
