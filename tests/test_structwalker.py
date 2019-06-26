from src.service.structwalker import StructWalker
from src.service.folderservice import FolderLister
from src.service.folderabs import FolderABS
from anytree import Node, RenderTree
import pytest, os


@pytest.fixture(scope="function")
def createfolders(tmpdir_factory):
    folder = tmpdir_factory.mktemp("rootfolder")
    file1 = folder.join("file1.txt")
    file1.write("content")

    file2 = folder.mkdir("folder1").join("file2.txt")
    file2.write("content")

    file3 = folder.mkdir("folder2").join("file3.txt")
    file3.write("content")

    folder.mkdir("folder3")
    t = folder.mkdir("folder4")
    subfolder4 = t.mkdir("subfolder4")
    file4 = subfolder4.join("file4.txt")
    file4.write("content")

    file5 = subfolder4.join("file5.txt")
    file5.write("content")

    return folder


@pytest.fixture(scope="function")
def fnlister():
    return FolderLister()


@pytest.fixture(scope="function")
def walker(fnlister):
    return StructWalker(fnlister)

@pytest.fixture(scope="function")
def walker2(fnlister):
    return StructWalker(fnlister)


def test_init_tree(walker):
    assert isinstance(walker.tree, Node)
    assert isinstance(walker.lister, FolderABS)
    assert walker.tree.name == ""
    assert walker.tree.__dict__["leaves"] == 0
    assert walker.counter == []


def test_transverse_struct(walker, createfolders):
    walker.transverse(createfolders.strpath, walker.tree)
    assert 5 == walker.tree.__dict__["leaves"]


def test_fix(walker, createfolders):
    rootfolder = createfolders.strpath
    walker.transverse(rootfolder, walker.tree)
    fixed = walker.fix(walker.tree)
    folders = {
        '': 5,
        f'{rootfolder}': 5,
        f'{rootfolder}{os.sep}folder1': 1,
        f'{rootfolder}{os.sep}folder2': 1,
        f'{rootfolder}{os.sep}folder3': 0,
        f'{rootfolder}{os.sep}folder4': 2,
        f'{rootfolder}{os.sep}folder4{os.sep}subfolder4': 2
    }
    for node in RenderTree(fixed):
        assert folders[node.node.name] == node.node.__dict__["leaves"]


def test_compare_trees(walker, walker2, createfolders):
    walker.transverse(createfolders.strpath, walker.tree)
    tree1 = walker.tree

    createfolders.mkdir("folder5")

    walker2.transverse(createfolders.strpath, walker2.tree)
    tree2 = walker2.tree

    # for f,i,node in RenderTree(tree1):
    #     print(node.name)

    # for f,i,node in RenderTree(tree2):
    #     print(node.name)
    print(os.path.abspath(createfolders.strpath+os.sep+'folder5'))
    print(walker.compareTrees(tree2, tree1))
    # assert '\\rootfolder2\\folder5' in walker.compareTrees(tree1, tree2)
