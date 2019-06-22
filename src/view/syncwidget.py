from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QCoreApplication, Qt
from collections import deque
from anytree import Node, RenderTree, LevelOrderIter
from src.service.structwalker import StructWalker
from src.service.wsapiservice import WSApi
from src.service.exceptions import WSApiException

class SyncWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(SyncWidget, self).__init__(parent)
        self.theadcount = 0
        self.parent = parent

        self.config = QSettings("application", "mainapp")
        self.config.sync()
        self.setObjectName("Form")
        self.resize(720, 647)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setCurrentIndex(0)

        self.assetTab = QtWidgets.QWidget()
        self.addAssetTab()

        self.settingsTab = QtWidgets.QWidget()
        self.addSettingTab()

        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self)
        self.setConfigs()

    def setConfigs(self):
        default = {
            'pamSource': '', 
            'pamDestination': '', 
            'watchFolder': '', 
            'username': '', 
            'password': '', 
            'wslInterplay': '', 
            'wslSdr': ''
        }
        self.pamSourceLineEdit.setText(self.config.value("mainapp", default)['pamSource'])
        self.pamDestinationLineEdit.setText(self.config.value("mainapp", default)['pamDestination'])
        self.watchFolderLineEdit.setText(self.config.value("mainapp", default)['watchFolder'])
        self.wslPamSourceLineEdit.setText(self.config.value("mainapp", default)['wslInterplay'])
        self.wslSdrLineEdit.setText(self.config.value("mainapp", default)['wslSdr'])
        self.usernameLineEdit.setText(self.config.value("mainapp", default)['username'])
        self.passwordLineEdit.setText(self.config.value("mainapp", default)['password'])

    def status(self, msg_text):
        self.parent.statusBar().showMessage(msg_text, 2000)

    def saveConfig(self):
        self.settings = {
            'pamSource': self.pamSourceLineEdit.text(),
            'pamDestination': self.pamDestinationLineEdit.text(),
            'watchFolder': self.watchFolderLineEdit.text(),
            'wslInterplay': self.wslPamSourceLineEdit.text(),
            'wslSdr': self.wslSdrLineEdit.text(),
            'username': self.usernameLineEdit.text(),
            'password': self.passwordLineEdit.text()
        }
        self.config.setValue("mainapp", self.settings)
        self.config.sync()
        self.status("Settings have been saved.")


    def addAssetTab(self):
        from src.view.interplaywidget import InterplayWidget

        self.interplayTreeView = InterplayWidget(self.assetTab)
        self.sdrTreeView = InterplayWidget(self.assetTab)

        self.updateBtn = QtWidgets.QPushButton(self.assetTab)
        self.updateBtn.clicked.connect(self.update)

        gridLayout = QtWidgets.QGridLayout(self.assetTab)
        gridLayout.addWidget(self.interplayTreeView, 0, 0, 1, 1)
        gridLayout.addWidget(self.sdrTreeView, 0, 1, 1, 1)
        gridLayout.addWidget(self.updateBtn, 1, 0, 1, 2)

        self.tabWidget.addTab(self.assetTab, "")

    def addSettingTab(self):
        self.interplayGBox = QtWidgets.QGroupBox(self.settingsTab)
        self.pamSourceLbl = QtWidgets.QLabel(self.interplayGBox)
        self.pamSourceLineEdit = QtWidgets.QLineEdit(self.interplayGBox)
        self.pamSourceLineEdit.setText("")
        self.pamDestinationLbl = QtWidgets.QLabel(self.interplayGBox)
        self.pamDestinationLineEdit = QtWidgets.QLineEdit(self.interplayGBox)
        self.watchFolderLbl = QtWidgets.QLabel(self.interplayGBox)
        self.watchFolderLineEdit = QtWidgets.QLineEdit(self.interplayGBox)

        interplayGLyt = QtWidgets.QGridLayout(self.interplayGBox)
        interplayGLyt.addWidget(self.pamSourceLbl, 0, 0, 1, 1)
        interplayGLyt.addWidget(self.pamSourceLineEdit, 0, 1, 1, 1)
        interplayGLyt.addWidget(self.pamDestinationLbl, 1, 0, 1, 1)
        interplayGLyt.addWidget(self.pamDestinationLineEdit, 1, 1, 1, 1)
        interplayGLyt.addWidget(self.watchFolderLbl, 2, 0, 1, 1)
        interplayGLyt.addWidget(self.watchFolderLineEdit, 2, 1, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.wsGBox = QtWidgets.QGroupBox(self.settingsTab)
        self.wslpamSourceLbl = QtWidgets.QLabel(self.wsGBox)
        self.usernameLbl = QtWidgets.QLabel(self.wsGBox)
        self.usernameLineEdit = QtWidgets.QLineEdit(self.wsGBox)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.wsGBox)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.wslPamSourceLineEdit = QtWidgets.QLineEdit(self.wsGBox)
        self.wslPamSourceLineEdit.setText("")
        self.passwordLbl = QtWidgets.QLabel(self.wsGBox)
        self.wslSdrLineEdit = QtWidgets.QLineEdit(self.wsGBox)
        self.wslSdrLbl = QtWidgets.QLabel(self.wsGBox)
        self.saveBtn = QtWidgets.QPushButton(self.settingsTab)
        self.saveBtn.clicked.connect(self.saveConfig)

        wsGLyt = QtWidgets.QGridLayout(self.wsGBox)
        wsGLyt.addWidget(self.wslpamSourceLbl, 0, 0, 1, 1)
        wsGLyt.addWidget(self.usernameLbl, 2, 0, 1, 1)
        wsGLyt.addWidget(self.usernameLineEdit, 2, 1, 1, 1)
        wsGLyt.addWidget(self.passwordLineEdit, 3, 1, 1, 1)
        wsGLyt.addWidget(self.wslPamSourceLineEdit, 0, 1, 1, 1)
        wsGLyt.addWidget(self.passwordLbl, 3, 0, 1, 1)
        wsGLyt.addWidget(self.wslSdrLineEdit, 1, 1, 1, 1)
        wsGLyt.addWidget(self.wslSdrLbl, 1, 0, 1, 1)

        verticalLayout = QtWidgets.QVBoxLayout(self.settingsTab)
        verticalLayout.addWidget(self.interplayGBox)
        verticalLayout.addItem(spacerItem)
        verticalLayout.addWidget(self.wsGBox)
        verticalLayout.addWidget(self.saveBtn)

        self.tabWidget.addTab(self.settingsTab, "")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
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

    def update(self):
        try:
            self.updateBtn.setEnabled(False)

            pam_source = self.pamSourceLineEdit.text()
            pam_destination = self.pamDestinationLineEdit.text()
            watch_folder = self.watchFolderLineEdit.text() 
            username = self.usernameLineEdit.text()
            password = self.passwordLineEdit.text()
            wsl_pam_source = self.wslPamSourceLineEdit.text()
            wsl_pam_destination = self.wslSdrLineEdit.text()

            self.interplayTreeView.update(pam_source, watch_folder, username, password, wsl_pam_source)
            self.interplayTreeView.threadsignal.connect(self.onFinished)
            self.sdrTreeView.update(pam_destination, watch_folder, username, password, wsl_pam_destination)
            self.sdrTreeView.threadsignal.connect(self.onFinished)

        except WSApiException as e:
            self.interplayTreeView.setEnabled(True)
            self.sdrTreeView.setEnabled(True)
            self.updateBtn.setEnabled(True)
            self.status(str(e))

    def onFinished(self):
        if self.interplayTreeView.threadfinished and self.sdrTreeView.threadfinished:
            self.updateBtn.setEnabled(True)


if __name__ == "__main__":
    import sys

    interplaydata = [
        {"name": "root", "level": 0, "leaves": 7, "parent": 'root'},
        {"name": "folder1", "level": 1, "leaves": 1, "parent": "root"},
        {"name": "folder2", "level": 1, "leaves": 0, "parent": "root"},
        {"name": "folder3", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "folder4", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "subfolder4", "level": 2, "leaves": 2, "parent": "folder4"}
    ]

    sdrdata = [
        {"name": "root", "level": 0, "leaves": 6, "parent": 'root'},
        {"name": "folder1", "level": 1, "leaves": 0, "parent": "root"},
        {"name": "folder2", "level": 1, "leaves": 0, "parent": "root"},
        {"name": "folder3", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "folder4", "level": 1, "leaves": 3, "parent": "root"},
        {"name": "subfolder4", "level": 2, "leaves": 2, "parent": "folder4"}
    ]

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = SyncWidget()
    ui.setupUi(Form, interplaydata, sdrdata)
    Form.show()
    sys.exit(app.exec_())
