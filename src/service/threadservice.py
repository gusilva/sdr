from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from src.service.structwalker import StructWalker
from anytree import LevelOrderIter

class WorkerThread(QObject):
    """
    Work class for threads.

    Methods
    -------
    setWalker(watchfolder, walker: StructWalker)
        Set instance attributes for the worker .
    """
    workersignal = pyqtSignal(str,list)

    def __init__(self):
        super().__init__()

    def setWalker(self, watchfolder, walker: StructWalker):
        self.walker = walker
        self.watchfolder = watchfolder

    def parse(self):
        mainfolder = self.watchfolder.split('/')[-1]
        return [{
            "name":node.name.replace(self.watchfolder, f'/{mainfolder}'), 
            "level": node.depth, 
            "leaves":node.__dict__["leaves"], 
            "parent": node.parent.name.replace(self.watchfolder, f'/{mainfolder}') if node.parent else node.name.replace(self.watchfolder, f'/{mainfolder}')
        } for node in LevelOrderIter(self.walker.tree)]

    @pyqtSlot()
    def run(self):
        print("worker has started")
        self.walker.transverse(self.watchfolder, self.walker.tree)
        self.walker.tree = self.walker.fix(self.walker.tree)
        datamodel = self.parse()
        self.workersignal.emit("finished", self.parse())