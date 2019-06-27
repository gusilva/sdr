from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from src.service.structwalker import StructWalker
from anytree import LevelOrderIter


class WorkerThread(QObject):
    """
    Work class for threads.

    Attributes
    ----------
    workersignal : pyqtSignal
        signal for the executed command.

    Methods
    -------
    setWalker(watchfolder: str, walker: StructWalker)
        Set instance attributes for the worker .

    parse()
        simple method to format the node names

    run()
        run the transverse command of the Structwalker object.     
    """

    workersignal = pyqtSignal(list)

    def __init__(self) -> None:
        """
        Inherit QObject constructor.

        """
        super().__init__()

    def setWalker(self, watchfolder: str, walker: StructWalker) -> None:
        """Set the necessary instance attributes.

        Parameters
        ----------
        watchfolder: str
            watch folder path.

        walker: StructWalker
            structwalker object.

        """
        self.walker = walker
        self.watchfolder = watchfolder

    def parse(self) -> list:
        """Format the node names.

        Returns
        -------
        list
            all nodes with name formated.
        """
        mainfolder = self.watchfolder.split("/")[-1]
        return [
            {
                "name": node.name.replace(self.watchfolder, f"/{mainfolder}"),
                "level": node.depth,
                "leaves": node.__dict__["leaves"],
                "parent": node.parent.name.replace(self.watchfolder, f"/{mainfolder}")
                if node.parent
                else node.name.replace(self.watchfolder, f"/{mainfolder}"),
            }
            for node in LevelOrderIter(self.walker.tree)
        ]

    @pyqtSlot()
    def run(self) -> None:
        """
        Run transverse method of StructWalker object.

        """
        self.walker.transverse(self.watchfolder, self.walker.tree)
        self.walker.tree = self.walker.fix(self.walker.tree)
        datamodel = self.parse()
        self.workersignal.emit(self.parse())
