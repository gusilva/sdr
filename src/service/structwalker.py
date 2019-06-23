from anytree import Node, RenderTree
from src.service.folderabs import FolderABS


class StructWalker(object):
    """
    A class to walk through folders tree.

    Methods
    -------
    transverse(foldername, parent = None)
        Walk through folders via recursion.

    fix(parent, count=0)
        Recalculate the root folders count.
    """

    def __init__(self, lister: FolderABS) -> None:
        """
        Parameters
        ----------
        lister : FolderABS
            Object that has listfolder method to list folders
            and files.
        """
        self.counter = []
        self.tree = Node("", leaves=0)
        self.lister = lister

    def transverse(self, foldername: str, parent: Node = None) -> Node:
        """Recursion through folder tree.

        It walks through folder tree systems.

        Parameters
        ----------
        foldername: str
            Root folder path.

        parent: Node
            Node object

        Returns
        -------
        Node
            Tree structure with the folders as Nodes.
        """
        elements, files = self.lister.listFolder(foldername)
        pt = Node(foldername, parent, leaves=len(files))

        self.counter.extend(files)

        if len(elements) == 0:
            parent.__dict__["leaves"] += len(files)
            return parent

        for el in elements:
            self.transverse(el, pt)

        if parent.is_root:
            parent.__dict__["leaves"] = len(self.counter)
            pt.__dict__["leaves"] = len(self.counter)

        return parent

    def fix(self, parent: Node, count: int = 0) -> Node:
        """Fix the folder count number.

        Parameters
        ----------
        parent: Node
            Node tree object.

        count: int
            Node object

        Returns
        -------
        Node
            Tree structure with the folders as Nodes.
        """
        if len(parent.children) == 0:
            return parent

        for node in parent.children:
            self.fix(node, count)
            if len(node.children) > 0:
                count = parent.__dict__["leaves"]
                parent.__dict__["leaves"] += node.__dict__["leaves"]
                if node.depth <= 2:
                    parent.__dict__["leaves"] = count

        return parent
