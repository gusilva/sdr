
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QThread, pyqtSignal
from src.service.wsapiservice import WSApi
from src.service.structwalker import StructWalker
from src.service.threadservice import WorkerThread
from anytree import Node
from collections import deque

class InterplayModel(QStandardItemModel):
    def __init__(self, parent=None):
        InterplayModel.__init__(self, parent)
        self.setHorizontalHeaderLabels(["Folders", "Count"])

class InterplayWidget(QTreeView):
    threadsignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(InterplayWidget, self).__init__(parent)
        self.setInterplayModel()
        self.setHeaderHidden(False)
        self.setSortingEnabled(True)
        self.header().setDefaultSectionSize(150)
        self.threadfinished = False

    def setInterplayModel(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Folders", "Count"])
        self.setModel(self.model)
        self.setCurrentIndex(self.model.index(0,0))

    def update(self, pam_source, watch_folder, username, password, wsl_pam_source):
        self.setEnabled(False)
        wsapi = WSApi(pam_source, watch_folder, username, password)
        wsapi.setClient(wsl_pam_source)
        walker = StructWalker(wsapi)
        walker.tree = Node(watch_folder, leaves=0)
        self.model.removeRows( 0, self.model.rowCount() )

        walker.counter = []
        walker.tree = Node(pam_source, leaves=0)

        self.worker = WorkerThread()
        self.worker.setWalker(watch_folder, walker)
        self.thread = QThread()
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.onFinished)
        self.worker.workersignal.connect(self.onWorkerSignal)
        self.worker.moveToThread(self.thread)
        self.thread.start()

    def onFinished(self):
        print("thread finished")
        self.threadfinished = True
        self.setEnabled(True)
        self.threadsignal.emit("finished")

    def onWorkerSignal(self, text, datamodel):
        self.threadfinished = False
        self.setTreeItems(datamodel)
        self.setEnabled(True)
        self.thread.terminate()

    def setTreeItems(self, data):
        seen = {}
        values = deque(data)
        while values:
            value = values.popleft()
            if value["level"] == 0:
                parent = self.model.invisibleRootItem()
            else:
                pid = value["parent"]
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            dbid = value["name"]
            parent.appendRow(
                [QStandardItem(value["name"]), QStandardItem(str(value["leaves"]))]
            )
            seen[dbid] = parent.child(parent.rowCount() - 1)
        