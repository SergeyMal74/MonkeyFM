import sys
import random

from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets


from mainwindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MainWindow()
    widget.show()

    sys.exit(app.exec_())