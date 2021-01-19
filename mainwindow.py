
import os
import sys
import random
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QAction, QToolBar, QFileSystemModel, QHeaderView, QAbstractItemView, QShortcut, QLineEdit, QSpacerItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSlot
from PyQt5.QtGui import QKeySequence

from fileview import FileView, FileViewSignals
from aboutdialog import AboutDialog
from keymanager import KeyManager, Sequence



class MainWindow(QtWidgets.QMainWindow):
    """
    Main window of application
    """

    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)

        self.toolBar = QToolBar()
        self.dockWidget.setTitleBarWidget(QtWidgets.QWidget(None))
        #self.setWindowTitle(self.titleGenerator())
        self.menuGenerator()
        self.toolBarGenerator()

        self.c = FileViewSignals.c
        self.c.changePath.connect(self.titleGenerate)
        self.c.changePath.connect(self.setPath)

        # Отображение файловой структуры в таблице
        self.view = FileView()

        #self.view.changePath.connect(self.titleGenerate)
        self.stackedWidget.insertWidget(0, self.view)
        self.stackedWidget.setCurrentIndex(0)

    def menuGenerator(self):
        """
        Функция генерации пунктов меню на панели
        """
        menuBar = self.menuBar()

        # Меню файл
        menuFile = menuBar.addMenu('File')
        menuFile.addAction('Create new folder')
        menuFile.addSeparator()
        # Выход
        exitAction = menuFile.addAction('Exit')
        exitAction.triggered.connect(self.exit)
        exitAction.setShortcut(QKeySequence(KeyManager.getSequence(Sequence.Exit)))
        # 'Браузерное' сочетание
        exitDirectionAction = QAction(self)
        self.addAction(exitDirectionAction)
        exitDirectionAction.triggered.connect(self.exit)
        exitDirectionAction.setShortcut(QKeySequence(KeyManager.getSequence(Sequence.ExitDirect)))

        menuEdit = menuBar.addMenu('Edit')
        menuView = menuBar.addMenu('View')
        menuGo = menuBar.addMenu('Go')
        menuBookmarks = menuBar.addMenu('Bookmarks')

        # Меню помощь
        menuHelp = menuBar.addMenu('Help')
        menuHelp.addAction('Keyboard shortcuts')
        menuHelp.addSeparator()
        aboutAction = menuHelp.addAction('About')
        aboutAction.triggered.connect(self.about)
        pass

    def toolBarGenerator(self):
        self.addToolBar(self.toolBar)
        toolBack = self.toolBar.addAction('Back')
        toolBack.triggered.connect(self.back)

        toolNext = self.toolBar.addAction('Next')
        toolNext.triggered.connect(self.next)
        toolUp = self.toolBar.addAction('Up')
        toolUp.triggered.connect(self.upper)

        emptyLeft = QWidget()
        emptyLeft.setMaximumWidth(20)
        emptyLeft.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        #self.toolBar.addWidget(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.toolBar.addWidget(emptyLeft)
        self.pathLine = QLineEdit()
        self.toolBar.addWidget(self.pathLine)
        emptyRight = QWidget()
        emptyRight.setMaximumWidth(20)
        emptyRight.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        #self.toolBar.addWidget(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.toolBar.addWidget(emptyRight)

        toolFind = self.toolBar.addAction('Find')
        toolFind.triggered.connect(self.find)
        findLine = QLineEdit()
        findLine.setMaximumWidth(300)
        self.toolBar.addWidget(findLine)

        pass

    def titleGenerator(self):
        """
        Функция генерации заголовка окна
        """
        currentFolder = self.view.getCurrentFolder()
        currentFolder = currentFolder.replace("/", "")
        return currentFolder
        pass
    
    def titleGenerate(self, path):
        basename = os.path.basename(path)
        if path == '/':
            self.setWindowTitle(path)
        elif len(basename) > 0:
            self.setWindowTitle(basename)
        else:
            self.setWindowTitle('Monkey file manager')
        pass

    def setPath(self, path):
        absolutePath = os.path.abspath(path)
        absolutePath = str(absolutePath).replace('//', '/')
        print(absolutePath)
        self.pathLine.setText(absolutePath)
        pass

    def runto(self):
        self.model.setRootPath("/tmp")
        pass

    def find(self):
        pass

    def createNewFolder(self):
        self.view.getCurrentFolder()
        # Create new folder
        pass

    def upper(self):
        self.view.goUp()
        pass

    def next(self):
        self.view.goNext()
        pass

    def back(self):
        self.view.goBack()
        pass

    def about(self):
        print('About')
        aboutDialog = AboutDialog(self)
        aboutDialog.show()
        pass

    def exit(self):
        """
        Выход из приложения
        """
        self.close()
        pass
