import pytest
import os
from embedia.tools import (FileRead, FileWrite, FileAppend, FileDelete, FileFolderMove,
                           FileFolderExists, FolderSearch, FolderCreate, FolderDelete,
                           FolderCopy, FolderList, FileCopy)
import shutil

shutil.rmtree('temp', ignore_errors=True)
shutil.rmtree('_temp', ignore_errors=True)
os.makedirs('temp')


@pytest.mark.asyncio
async def test_fileops(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')

    filewrite = FileWrite()
    fileread = FileRead()
    fileappend = FileAppend()
    filedelete = FileDelete()
    filemove = FileFolderMove()
    filecopy = FileCopy()
    fileexists = FileFolderExists()
    foldersearch = FolderSearch()
    foldercreate = FolderCreate()
    folderdelete = FolderDelete()
    foldercopy = FolderCopy()
    folderlist = FolderList()

    await filewrite('temp/1.txt', 'Hello World!')
    await filewrite('temp/1.txt', 'Hello World!')

    output = await fileread('temp/1.txt')
    assert isinstance(output[0], str)
    assert len(output[0]) == 12

    await fileappend('temp/1.txt', 'Hello World!')
    await fileappend('temp/2.txt', 'Hello World!')

    output = await fileread('temp/1.txt')
    assert isinstance(output[0], str)
    assert len(output[0]) == 24

    output = await fileread('temp/2.txt')
    assert isinstance(output[0], str)
    assert len(output[0]) == 12

    await filedelete('temp/1.txt')

    with pytest.raises(FileNotFoundError):
        await fileread('temp/1.txt')

    with pytest.raises(FileNotFoundError):
        await filedelete('temp/1.txt')

    with pytest.raises(IsADirectoryError):
        await filedelete('temp')

    await filemove('temp/2.txt', 'temp/1.txt')

    output = await fileread('temp/1.txt')
    assert isinstance(output[0], str)
    assert len(output[0]) == 12

    with pytest.raises(FileNotFoundError):
        await filemove('temp/2.txt', 'temp/1.txt')

    with pytest.raises(FileNotFoundError):
        await filemove('temp/1.txt', '_temp/1.txt')

    await filecopy('temp/1.txt', 'temp/2.txt')
    output = await fileread('temp/2.txt')
    assert isinstance(output[0], str)
    assert len(output[0]) == 12

    with pytest.raises(FileNotFoundError):
        await filecopy('temp/1.txt', '_temp/2.txt')

    with pytest.raises(FileNotFoundError):
        await filecopy('temp/3.txt', 'temp/4.txt')

    with pytest.raises(FileNotFoundError):
        await filecopy('temp/3.txt', 'temp/2.txt')

    with pytest.raises(IsADirectoryError):
        await filecopy('temp', '_temp')

    await fileappend('temp/2.txt', 'Hello World!')
    await filecopy('temp/2.txt', 'temp/1.txt')
    output = await fileread('temp/1.txt')
    assert isinstance(output[0], str)
    assert len(output[0]) == 24

    out = await fileexists('temp')
    assert out[0] is True

    out = await fileexists('temp/1.txt')
    assert out[0] is True

    out = await fileexists('temp/3.txt')
    assert out[0] is False

    out = await foldersearch('temp', '1.txt')
    assert out[0] == 'temp/1.txt'

    await foldercreate('temp/subtemp')
    out = await fileexists('temp/subtemp')
    assert out[0] is True

    await filecopy('temp/1.txt', 'temp/subtemp/3.txt')
    out = await foldersearch('temp', '3.txt')
    assert out[0] == 'temp/subtemp/3.txt'

    await folderdelete('temp/subtemp')
    out = await fileexists('temp/subtemp')
    assert out[0] is False

    with pytest.raises(NotADirectoryError):
        await folderdelete('temp/2.txt')

    await filemove('temp', '_temp')
    out = await fileexists('_temp')
    assert out[0] is True

    await foldercopy('_temp', 'temp')
    out = await fileexists('temp')
    assert out[0] is True

    with pytest.raises(FileExistsError):
        await foldercopy('_temp', 'temp')

    with pytest.raises(NotADirectoryError):
        await foldercopy('_temp/1.txt', 'temp')

    with pytest.raises(NotADirectoryError):
        await foldercopy('_temp', 'temp/3.txt')

    out = await folderlist('temp')
    assert set(out[0]).issuperset({'1.txt', '2.txt'})

    with pytest.raises(NotADirectoryError):
        await folderlist('temp/1.txt')

    shutil.rmtree('temp', ignore_errors=True)
    shutil.rmtree('_temp', ignore_errors=True)
