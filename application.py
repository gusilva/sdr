"""SDR Validator

Usage:
  application.py [-v] [--config=<configfile>]

Options:
    -h, --help
    -v, --verbose

"""
from docopt import docopt

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QCoreApplication, QSize
from src.view.syncwidget import SyncWidget
import src.resource.sdrico
import configparser
import sys


if sys.platform.startswith("win"):
    import ctypes

    appid = "tvglobo.sdrmonitor.ver1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

QCoreApplication.setApplicationName("SDR MONITOR")
QCoreApplication.setOrganizationDomain("tvglobo.com.br")


class MainWindow(QMainWindow):
    """
    Main Window to group all widgets.

    """

    def __init__(self, parent: QMainWindow = None):
        """
        Inherit QMainWindow constructor and configure the widget.

        Parameters
        ----------
        parent : QMainWindow
            parent widget object

        """
        super(MainWindow, self).__init__(parent)
        app_ico = QIcon()
        app_ico.addFile(":/icons/monitoring16x16.ico", QSize(16, 16))
        app_ico.addFile(":/icons/monitoring32x32.ico", QSize(32, 32))
        app_ico.addFile(":/icons/monitoring48x48.ico", QSize(48, 48))
        app_ico.addFile(":/icons/monitoring64x64.ico", QSize(64, 64))
        app_ico.addFile(":/icons/monitoring96x96.ico", QSize(96, 96))
        app_ico.addFile(":/icons/monitoring128x128.ico", QSize(128, 128))
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
            app = QApplication(sys.argv)
            ui = MainWindow()
            ui.show()
            sys.exit(app.exec_())
    except Exception as e:
        from traceback import format_exc

        print("A error occured: {}".format(format_exc(e)))
