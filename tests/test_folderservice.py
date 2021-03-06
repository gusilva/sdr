import pytest, os
from src.service.folderservice import FolderLister


@pytest.fixture(scope="session")
def rootfolder(tmpdir_factory):
    folder = tmpdir_factory.mktemp("rootfolder")
    file1 = folder.join("file1.txt")

    folder.mkdir("folder1")
    file1.write("content")
    return folder


def test_listfolders(rootfolder):
    f = FolderLister()

    folders, files = f.listFolder(rootfolder.strpath)
    assert len(folders) == 1
    assert f'{rootfolder.strpath}{os.sep}folder1' in folders
    assert len(files) == 1
    assert "file1.txt" == files[0].split(f"{os.sep}")[-1]

    rootfolder.mkdir("folder2")

    folders, files = f.listFolder(rootfolder.strpath)

    assert len(folders) == 2
    assert f'{rootfolder.strpath}{os.sep}folder1' in folders
    assert f'{rootfolder.strpath}{os.sep}folder2' in folders
    assert len(files) == 1
    assert "file1.txt" == files[0].split(f"{os.sep}")[-1]

    file2 = rootfolder.join("file2.txt").write("file2")
    file3 = rootfolder.join("file3.txt").write("file3")

    folders, files = f.listFolder(rootfolder.strpath)
    assert len(folders) == 2
    assert f'{rootfolder.strpath}{os.sep}folder1' in folders
    assert f'{rootfolder.strpath}{os.sep}folder2' in folders
    assert len(files) == 3
    assert f'{rootfolder.strpath}{os.sep}file1.txt' in files
    assert f'{rootfolder.strpath}{os.sep}file2.txt' in files
    assert f'{rootfolder.strpath}{os.sep}file3.txt' in files
