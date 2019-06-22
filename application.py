"""SDR Validator

Usage:
  application.py [-v] [--config=<configfile>]

Options:
    -h, --help
    -v, --verbose

"""
from docopt import docopt
import configparser
import sys, os
from src.view.syncwidget import SyncWidget
import src.resource.sdrico
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
import ctypes

appid = 'tvglobo.sdrmonitor.ver1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

QCoreApplication.setApplicationName("SDR MONITOR")
QCoreApplication.setOrganizationDomain("tvglobo.com.br")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        app_ico = QtGui.QIcon()
        app_ico.addFile(':/icons/monitoring16x16.ico', QtCore.QSize(16,16))
        app_ico.addFile(':/icons/monitoring32x32.ico', QtCore.QSize(32,32))
        app_ico.addFile(':/icons/monitoring48x48.ico', QtCore.QSize(48,48))
        app_ico.addFile(':/icons/monitoring64x64.ico', QtCore.QSize(64,64))
        app_ico.addFile(':/icons/monitoring96x96.ico', QtCore.QSize(96,96))
        app_ico.addFile(':/icons/monitoring128x128.ico', QtCore.QSize(128,128))
        self.form_widget = SyncWidget(self)
        self.setCentralWidget(self.form_widget)
        self.setWindowIcon(app_ico)

if __name__ == "__main__":
    try:
        arguments = docopt(__doc__)

        if arguments["--config"]:
            from src.service.cliservice import CliService

            config = configparser.ConfigParser()
            config.read(arguments["--config"])
            user = config["Credentials"]["User"]
            pwd = config["Credentials"]["Password"]
            dbip = config["DB"]["DBIP"]
            dbtable = config["DB"]["DBTABLE"]
            dbuser = config["DB"]["User"]
            dbpwd = config["DB"]["Password"]

            executor = CliService(user, pwd, dbip, dbtable, dbuser, dbpwd)
            executor.run()

        else:
            app = QtWidgets.QApplication(sys.argv)
            ui = MainWindow()
            ui.show()
            sys.exit(app.exec_())
    except Exception as e:
        from traceback import format_exc
        print("A error occured: {}".format(format_exc(e)))
 
