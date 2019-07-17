from PyQt5.QtWidgets import QTreeView, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QThread, pyqtSignal
from src.service.wsapiservice import WSApi
from src.service.structwalker import StructWalker
from src.service.threadservice import WorkerThread
from anytree import Node
from collections import deque


class InterplayWidget(QTreeView):
    """
    Interplay widget for the ui.

    Attributes
    ----------
    threadsignal : pyqtSignal
        signal for when the worker has returned the data.

    Methods
    -------
    setInterplayModel()
        create and set the model data.

    update(pam_source: str, watch_folder: str, username: str, password: str, wsl_pam: str)
        dispatch the threads to get data for the tree widget.

    onFinished()
        Enable the tree widget and emit the finish signal.

    onWorkerSignal(datamodel: list)
        retrieve the data when worker has finished.

    setTreeItems(data: list)
        set the tree widget data.
    """

    threadsignal = pyqtSignal(str)

    def __init__(self, parent: QWidget = None) -> None:
        """
        Inherit QTreeView constructor and configure the widget.

        Parameters
        ----------
        parent : QWidget
            parent widget object

        """
        super(InterplayWidget, self).__init__(parent)
        self.setInterplayModel()
        self.setHeaderHidden(False)
        self.setSortingEnabled(True)
        self.header().setDefaultSectionSize(150)
        self.threadfinished = False

    def setInterplayModel(self) -> None:
        """
        Create and configure the model data to be used in treewidget.

        """
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Folders", "Count"])
        self.setModel(self.model)
        self.setCurrentIndex(self.model.index(0, 0))

    def update(
        self,
        pam_source: str,
        watch_folder: str,
        username: str,
        password: str,
        wsl_pam: str,
    ) -> None:
        """
        Dispatch the threads to get data for the tree widget.

        Parameters
        ----------
        pam_source : str
            production asset management source.

        watch_folder : str
            watch folder path.

        username : str
            username to access pam resources.

        password : str
            password for the username.

        wsl_pam : str
            url for webservice description language server.

        """
        self.setEnabled(False)
        self.wsapi = WSApi(pam_source, watch_folder, username, password)
        self.wsapi.setClient(wsl_pam)
        self.walker = StructWalker(self.wsapi)
        self.walker.tree = Node(watch_folder, leaves=0)
        self.model.removeRows(0, self.model.rowCount())

        self.walker.counter = []
        self.walker.tree = Node(pam_source, leaves=0)

        self.worker = WorkerThread()
        self.worker.setWalker(watch_folder, self.walker)
        self.thread = QThread()
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.onFinished)
        self.worker.workersignal.connect(self.onWorkerSignal)
        self.worker.moveToThread(self.thread)
        self.thread.start()

    def onFinished(self) -> None:
        """
        Enable the tree widget and emit the finish signal.

        """
        self.threadfinished = True
        self.setEnabled(True)
        self.threadsignal.emit("finished")

    def onWorkerSignal(self, datamodel: list) -> None:
        """
        Retrieve the data when worker has finished.

        Parameters
        ----------
        datamodel : list
            model data with all nodes.

        """
        self.threadfinished = False
        self.setTreeItems(datamodel)
        self.setEnabled(True)
        self.thread.terminate()

    def setTreeItems(self, data: list) -> None:
        """
        Set the tree widget data.

        Parameters
        ----------
        data : list
            model data with all nodes.

        """
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
