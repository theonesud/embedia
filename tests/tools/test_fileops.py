import os
import shutil

import pytest
from embedia.tools import (
    FileAppend,
    FileCopy,
    FileDelete,
    FileFolderExists,
    FileFolderMove,
    FileRead,
    FileWrite,
    FolderCopy,
    FolderCreate,
    FolderDelete,
    FolderList,
    FolderSearch,
)


@pytest.mark.asyncio
async def test_fileops(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")

    shutil.rmtree("temp", ignore_errors=True)
    os.makedirs("temp")

    foldercreate = FolderCreate()
    filewrite = FileWrite()

    filecopy = FileCopy()
    foldercopy = FolderCopy()
    filemove = FileFolderMove()

    fileexists = FileFolderExists()
    foldersearch = FolderSearch()
    folderlist = FolderList()

    fileappend = FileAppend()

    fileread = FileRead()

    filedelete = FileDelete()
    folderdelete = FolderDelete()

    with pytest.raises(FileNotFoundError):
        await fileread("temp/unknown.txt")

    with pytest.raises(FileNotFoundError):
        await filedelete("temp/unknown.txt")

    await foldercreate("temp/subtemp")
    out = await fileexists("temp/subtemp")
    assert out.output is True

    # with pytest.raises(IsADirectoryError):
    #     await filedelete('./temp')

    await filewrite("temp/1.txt", "Hello World!")
    await fileappend("temp/1.txt", ">>>")
    out = await fileread("temp/1.txt")
    assert out.output == "Hello World!>>>"

    with pytest.raises(FileNotFoundError):
        await filemove("temp/unknown.txt", "temp/1.txt")

    with pytest.raises(FileNotFoundError):
        await filemove("temp/1.txt", "unknown/1.txt")

    with pytest.raises(FileNotFoundError):
        await filecopy("temp/1.txt", "unknown/1.txt")

    with pytest.raises(FileNotFoundError):
        await filecopy("temp/unknown.txt", "temp/2.txt")

    with pytest.raises(IsADirectoryError):
        await filecopy("temp", "temp/subtemp")

    with pytest.raises(NotADirectoryError):
        await folderdelete("temp/1.txt")

    await filecopy("temp/1.txt", "temp/subtemp/1.txt")
    out = await fileread("temp/subtemp/1.txt")
    assert out.output == "Hello World!>>>"

    await foldercopy("temp/subtemp", "temp/subtemp2")
    out = await fileread("temp/subtemp2/1.txt")
    assert out.output == "Hello World!>>>"

    with pytest.raises(FileExistsError):
        await foldercopy("temp/subtemp", "temp/subtemp2")

    with pytest.raises(NotADirectoryError):
        await foldercopy("temp/1.txt", "temp2")

    # edgecase: creates a folder called '3.txt'
    await foldercopy("temp", "temp/3.txt")

    await filemove("temp/subtemp2/1.txt", "temp/subtemp/2.txt")
    out = await fileread("temp/subtemp/2.txt")
    assert out.output == "Hello World!>>>"

    out = await folderlist("temp/subtemp")
    assert set(out.output) == {"1.txt", "2.txt"}

    with pytest.raises(NotADirectoryError):
        await folderlist("temp/1.txt")

    out = await foldersearch("temp/subtemp", "2.txt")
    assert out.output == "temp/subtemp/2.txt"

    await filedelete("temp/subtemp/2.txt")
    out = await fileexists("temp/subtemp/2.txt")
    assert out.output is False

    await folderdelete("temp/subtemp")
    out = await fileexists("temp/subtemp")
    assert out.output is False

    shutil.rmtree("temp")
