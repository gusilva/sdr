from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import QSettings, QCoreApplication, Qt, QMetaObject
from PyQt5.QtGui import QColor
from datetime import datetime, timezone
from collections import deque
from src.service.structwalker import StructWalker
from src.service.wsapiservice import WSApi
from src.service.exceptions import WSApiException
from src.view.interplaywidget import InterplayWidget


class SyncWidget(QWidget):
    """
    Sync ui with the interplay tree widgets.

    Methods
    -------
    setConfigs()
        set the settings tab with saved data.

    status(msg_text: str)
        set the statusbar text.

    saveConfig()
        save configs from settings tab.

    addAssetTab()
        add tab widget with the interplaytree widgets.

    addSettingTab()
        add settings tab widget.

    retranslateUi()
        translate method for the texts.

    update()
        update the interplaytree when the update button is pressed.

    onFinished()
        enable the update button.

    """

    def __init__(self, parent: QWidget) -> None:
        """
        Inherit QWidget constructor and configure the widget.

        Parameters
        ----------
        parent : QWidget
            parent widget object

        """
        super(SyncWidget, self).__init__(parent)
        self.theadcount = 0
        self.parent = parent

        self.config = QSettings("application", "mainapp")
        self.config.sync()
        self.setObjectName("Form")
        self.resize(720, 647)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setCurrentIndex(0)

        self.assetTab = QWidget()
        self.addAssetTab()

        self.settingsTab = QWidget()
        self.addSettingTab()

        verticalLayout = QVBoxLayout(self)
        verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)
        self.setConfigs()

    def setConfigs(self) -> None:
        """
        Set the settings tab with saved data.

        """
        default = {
            "pamSource": "",
            "pamDestination": "",
            "watchFolder": "",
            "username": "",
            "password": "",
            "wslInterplay": "",
            "wslSdr": "",
        }
        self.pamSourceLineEdit.setText(
            self.config.value("mainapp", default)["pamSource"]
        )
        self.pamDestinationLineEdit.setText(
            self.config.value("mainapp", default)["pamDestination"]
        )
        self.watchFolderLineEdit.setText(
            self.config.value("mainapp", default)["watchFolder"]
        )
        self.wslPamSourceLineEdit.setText(
            self.config.value("mainapp", default)["wslInterplay"]
        )
        self.wslSdrLineEdit.setText(self.config.value("mainapp", default)["wslSdr"])
        self.usernameLineEdit.setText(self.config.value("mainapp", default)["username"])
        self.passwordLineEdit.setText(self.config.value("mainapp", default)["password"])

    def status(self, msg_text: str) -> None:
        """Set the statusbar text.

        Parameters
        ----------
        msg_text : str
            message to be shown in statusbar.

        """
        self.parent.statusBar().showMessage(msg_text, 2000)

    def saveConfig(self) -> None:
        """
        Save configs from settings tab.

        """
        self.settings = {
            "pamSource": self.pamSourceLineEdit.text(),
            "pamDestination": self.pamDestinationLineEdit.text(),
            "watchFolder": self.watchFolderLineEdit.text(),
            "wslInterplay": self.wslPamSourceLineEdit.text(),
            "wslSdr": self.wslSdrLineEdit.text(),
            "username": self.usernameLineEdit.text(),
            "password": self.passwordLineEdit.text(),
        }
        self.config.setValue("mainapp", self.settings)
        self.config.sync()
        self.status("Settings have been saved.")

    def addAssetTab(self) -> None:
        """
        Add tab widget with the interplaytree widgets.

        """
        self.interplayTreeView = InterplayWidget(self.assetTab)
        self.sdrTreeView = InterplayWidget(self.assetTab)

        self.updateBtn = QPushButton(self.assetTab)
        self.updateBtn.clicked.connect(self.update)

        gridLayout = QGridLayout(self.assetTab)
        gridLayout.addWidget(self.interplayTreeView, 0, 0, 1, 1)
        gridLayout.addWidget(self.sdrTreeView, 0, 1, 1, 1)
        gridLayout.addWidget(self.updateBtn, 1, 0, 1, 2)

        self.tabWidget.addTab(self.assetTab, "")

    def addSettingTab(self) -> None:
        """
        Add settings tab widget.

        """
        self.interplayGBox = QGroupBox(self.settingsTab)
        self.pamSourceLbl = QLabel(self.interplayGBox)
        self.pamSourceLineEdit = QLineEdit(self.interplayGBox)
        self.pamSourceLineEdit.setText("")
        self.pamDestinationLbl = QLabel(self.interplayGBox)
        self.pamDestinationLineEdit = QLineEdit(self.interplayGBox)
        self.watchFolderLbl = QLabel(self.interplayGBox)
        self.watchFolderLineEdit = QLineEdit(self.interplayGBox)

        interplayGLyt = QGridLayout(self.interplayGBox)
        interplayGLyt.addWidget(self.pamSourceLbl, 0, 0, 1, 1)
        interplayGLyt.addWidget(self.pamSourceLineEdit, 0, 1, 1, 1)
        interplayGLyt.addWidget(self.pamDestinationLbl, 1, 0, 1, 1)
        interplayGLyt.addWidget(self.pamDestinationLineEdit, 1, 1, 1, 1)
        interplayGLyt.addWidget(self.watchFolderLbl, 2, 0, 1, 1)
        interplayGLyt.addWidget(self.watchFolderLineEdit, 2, 1, 1, 1)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.wsGBox = QGroupBox(self.settingsTab)
        self.wslpamSourceLbl = QLabel(self.wsGBox)
        self.usernameLbl = QLabel(self.wsGBox)
        self.usernameLineEdit = QLineEdit(self.wsGBox)
        self.passwordLineEdit = QLineEdit(self.wsGBox)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.wslPamSourceLineEdit = QLineEdit(self.wsGBox)
        self.wslPamSourceLineEdit.setText("")
        self.passwordLbl = QLabel(self.wsGBox)
        self.wslSdrLineEdit = QLineEdit(self.wsGBox)
        self.wslSdrLbl = QLabel(self.wsGBox)
        self.saveBtn = QPushButton(self.settingsTab)
        self.saveBtn.clicked.connect(self.saveConfig)

        wsGLyt = QGridLayout(self.wsGBox)
        wsGLyt.addWidget(self.wslpamSourceLbl, 0, 0, 1, 1)
        wsGLyt.addWidget(self.usernameLbl, 2, 0, 1, 1)
        wsGLyt.addWidget(self.usernameLineEdit, 2, 1, 1, 1)
        wsGLyt.addWidget(self.passwordLineEdit, 3, 1, 1, 1)
        wsGLyt.addWidget(self.wslPamSourceLineEdit, 0, 1, 1, 1)
        wsGLyt.addWidget(self.passwordLbl, 3, 0, 1, 1)
        wsGLyt.addWidget(self.wslSdrLineEdit, 1, 1, 1, 1)
        wsGLyt.addWidget(self.wslSdrLbl, 1, 0, 1, 1)

        verticalLayout = QVBoxLayout(self.settingsTab)
        verticalLayout.addWidget(self.interplayGBox)
        verticalLayout.addItem(spacerItem)
        verticalLayout.addWidget(self.wsGBox)
        verticalLayout.addWidget(self.saveBtn)

        self.tabWidget.addTab(self.settingsTab, "")

    def retranslateUi(self) -> None:
        """
        Translate method for the texts.

        """
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("SDR MONITOR", "SDR MONITOR"))

        self.updateBtn.setText(_translate("Form", "Update"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.assetTab), _translate("Form", "Assets")
        )
        self.interplayGBox.setTitle(_translate("Form", "INTERPLAY"))
        self.pamSourceLbl.setText(_translate("Form", "PAM SOURCE"))
        self.pamDestinationLbl.setText(_translate("Form", "PAM DESTINATION"))
        self.watchFolderLbl.setText(_translate("Form", "WATCHFOLDER"))
        self.wsGBox.setTitle(_translate("Form", "WEBSERVICE"))
        self.wslpamSourceLbl.setText(_translate("Form", "WSL INTERPLAY"))
        self.usernameLbl.setText(_translate("Form", "USERNAME"))
        self.passwordLbl.setText(_translate("Form", "PASSWORD"))
        self.wslSdrLbl.setText(_translate("Form", "WSL SDR"))
        self.saveBtn.setText(_translate("Form", "Save"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.settingsTab), _translate("Form", "Settings")
        )

    def update(self) -> None:
        """
        Update the interplaytree when the update button is pressed.

        """
        try:
            self.updateBtn.setEnabled(False)

            pam_source = self.pamSourceLineEdit.text()
            pam_destination = self.pamDestinationLineEdit.text()
            watch_folder = self.watchFolderLineEdit.text()
            username = self.usernameLineEdit.text()
            password = self.passwordLineEdit.text()
            wsl_pam_source = self.wslPamSourceLineEdit.text()
            wsl_pam_destination = self.wslSdrLineEdit.text()

            self.interplayTreeView.update(
                pam_source, watch_folder, username, password, wsl_pam_source
            )
            self.interplayTreeView.threadsignal.connect(self.onFinished)
            self.sdrTreeView.update(
                pam_destination, watch_folder, username, password, wsl_pam_destination
            )
            self.sdrTreeView.threadsignal.connect(self.onFinished)

        except WSApiException as e:
            self.interplayTreeView.setEnabled(True)
            self.sdrTreeView.setEnabled(True)
            self.updateBtn.setEnabled(True)
            self.status(str(e))

    def onFinished(self) -> None:
        """
        Enable the update button.

        """
        if self.interplayTreeView.threadfinished and self.sdrTreeView.threadfinished:
            self.getMissingFolders()
            self.updateBtn.setEnabled(True)
            self.interplayTreeView.threadfinished = False
            self.sdrTreeView.threadfinished = False

    def setColorNotOldThan(
        self, days: int, mainfolder: str, dif: set, color: str, pam_obj: InterplayWidget
    ) -> None:
        """Set tree items color to items older than days.

        Parameters
        ----------
        days : int
            days that the folder has not been modified.

        mainfolder : str
            root path.

        dif : set
            set of folders that differs from another tree structure.

        color : str
            color to mark down.

        pam_obj : InterplayWidget
            interplay widget object.

        """
        t1 = datetime.now(timezone.utc)
        for i in dif:
            r = i.replace(mainfolder, "")
            t2 = pam_obj.wsapi.getAssetDate(i)
            tdelta = t1 - t2
            if tdelta.days >= days:
                h = pam_obj.model.findItems(r, Qt.MatchRecursive)
                h[0].setBackground(QColor(color))

    def getMissingFolders(self) -> None:
        """Get missing folders and set item colors.

        """
        pam_source_tree = self.interplayTreeView.walker.tree
        pam_destination_tree = self.sdrTreeView.walker.tree
        dif = self.interplayTreeView.walker.compareTrees(
            pam_source_tree, pam_destination_tree
        )
        dif_sdr = self.interplayTreeView.walker.compareTrees(
            pam_destination_tree, pam_source_tree
        )
        watch_folder = self.watchFolderLineEdit.text().split("/")
        watch_folder.pop(-1)
        watch_folder = "/".join(watch_folder)
        self.setColorNotOldThan(2, watch_folder, dif, "red", self.interplayTreeView)
        self.setColorNotOldThan(2, watch_folder, dif_sdr, "yellow", self.sdrTreeView)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    interplaydata = [
        {"name": "root", "level": 0, "leaves": 7, "parent": "root"},
        {"name": "folder1", "level": 1, "leaves": 1, "parent": "root"},
        {"name": "folder2", "level": 1, "leaves": 0, "parent": "root"},
        {"name": "folder3", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "folder4", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "subfolder4", "level": 2, "leaves": 2, "parent": "folder4"},
    ]

    sdrdata = [
        {"name": "root", "level": 0, "leaves": 6, "parent": "root"},
        {"name": "folder1", "level": 1, "leaves": 0, "parent": "root"},
        {"name": "folder2", "level": 1, "leaves": 0, "parent": "root"},
        {"name": "folder3", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "folder4", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "subfolder4", "level": 2, "leaves": 2, "parent": "folder4"},
    ]

    app = QApplication(sys.argv)
    Form = QWidget()
    ui = SyncWidget()
    ui.setupUi(Form, interplaydata, sdrdata)
    Form.show()
    sys.exit(app.exec_())
