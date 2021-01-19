
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QWidget, QDialog, QPushButton

class AboutDialog(QDialog):
    """
    О программе
    """
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('aboutdialog.ui', self)
        self.setWindowTitle('About')

        self.pb_ok.clicked.connect(self.exit)
        self.pb_licence.clicked.connect(self.exit)
        pass

    def licence(self):
        pass

    def exit(self):
        self.close()
        pass
