import pytest
import os
from embedia.tools.fileops import FileRead, FileWrite, FileAppend, FileDelete, FileFolderMove
from embedia.tools.fileops import FileFolderExists, FolderSearch, FolderCreate, FolderDelete
from embedia.tools.fileops import FolderCopy, FolderList, FileCopy
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

    await filewrite.run('temp/1.txt', 'Hello World!')
    await filewrite.run('temp/1.txt', 'Hello World!')

    output = await fileread.run('temp/1.txt')
    assert isinstance(output, str)
    assert len(output) == 12

    await fileappend.run('temp/1.txt', 'Hello World!')
    await fileappend.run('temp/2.txt', 'Hello World!')

    output = await fileread.run('temp/1.txt')
    assert isinstance(output, str)
    assert len(output) == 24

    output = await fileread.run('temp/2.txt')
    assert isinstance(output, str)
    assert len(output) == 12

    await filedelete.run('temp/1.txt')

    with pytest.raises(FileNotFoundError):
        await fileread.run('temp/1.txt')

    with pytest.raises(FileNotFoundError):
        await filedelete.run('temp/1.txt')

    with pytest.raises(IsADirectoryError):
        await filedelete.run('temp')

    await filemove.run('temp/2.txt', 'temp/1.txt')

    output = await fileread.run('temp/1.txt')
    assert isinstance(output, str)
    assert len(output) == 12

    with pytest.raises(FileNotFoundError):
        await filemove.run('temp/2.txt', 'temp/1.txt')

    with pytest.raises(FileNotFoundError):
        await filemove.run('temp/1.txt', '_temp/1.txt')

    await filecopy.run('temp/1.txt', 'temp/2.txt')
    output = await fileread.run('temp/2.txt')
    assert isinstance(output, str)
    assert len(output) == 12

    with pytest.raises(FileNotFoundError):
        await filecopy.run('temp/1.txt', '_temp/2.txt')

    with pytest.raises(FileNotFoundError):
        await filecopy.run('temp/3.txt', 'temp/4.txt')

    with pytest.raises(FileNotFoundError):
        await filecopy.run('temp/3.txt', 'temp/2.txt')

    with pytest.raises(IsADirectoryError):
        await filecopy.run('temp', '_temp')

    await fileappend.run('temp/2.txt', 'Hello World!')
    await filecopy.run('temp/2.txt', 'temp/1.txt')
    output = await fileread.run('temp/1.txt')
    assert isinstance(output, str)
    assert len(output) == 24

    out = await fileexists.run('temp')
    assert out is True

    out = await fileexists.run('temp/1.txt')
    assert out is True

    out = await fileexists.run('temp/3.txt')
    assert out is False

    out = await foldersearch.run('temp', '1.txt')
    assert out == 'temp/1.txt'

    await foldercreate.run('temp/subtemp')
    out = await fileexists.run('temp/subtemp')
    assert out is True

    await filecopy.run('temp/1.txt', 'temp/subtemp/3.txt')
    out = await foldersearch.run('temp', '3.txt')
    assert out == 'temp/subtemp/3.txt'

    await folderdelete.run('temp/subtemp')
    out = await fileexists.run('temp/subtemp')
    assert out is False

    with pytest.raises(NotADirectoryError):
        await folderdelete.run('temp/2.txt')

    await filemove.run('temp', '_temp')
    out = await fileexists.run('_temp')
    assert out is True

    await foldercopy.run('_temp', 'temp')
    out = await fileexists.run('temp')
    assert out is True

    with pytest.raises(FileExistsError):
        await foldercopy.run('_temp', 'temp')

    with pytest.raises(NotADirectoryError):
        await foldercopy.run('_temp/1.txt', 'temp')

    with pytest.raises(NotADirectoryError):
        await foldercopy.run('_temp', 'temp/3.txt')

    out = await folderlist.run('temp')
    assert set(out).issuperset({'1.txt', '2.txt'})

    with pytest.raises(NotADirectoryError):
        await folderlist.run('temp/1.txt')

    shutil.rmtree('temp', ignore_errors=True)
    shutil.rmtree('_temp', ignore_errors=True)
