
import os
import sys
import random
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QAction, QToolBar, QFileSystemModel, QHeaderView, QAbstractItemView, QShortcut, QLineEdit, QSpacerItem
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDir, pyqtSlot
from PyQt5.QtGui import QKeySequence

from fileview import FileView
from aboutdialog import AboutDialog
from keymanager import KeyManager, Sequence

from filemodel import FileModel
from placemodel import PlaceModel

class MainWindow(QtWidgets.QMainWindow):
    """
    Main window of application
    """

    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        
        self.model = FileModel()
        self.view = FileView()

        placemodel = PlaceModel(self.treeView)
        self.treeView.setModel(placemodel)
        self.treeView.expandAll()

        self.view.setModel(self.model)

        self.stackedWidget.insertWidget(0, self.view)
        self.stackedWidget.setCurrentIndex(0)

        self.dockWidget.setTitleBarWidget(QtWidgets.QWidget(None))
        self.menuGenerator()
        self.toolBar = QToolBar()
        self.toolBarGenerator()

    def menuGenerator(self):
        """
        Функция генерации пунктов меню на панели
        """
        menuBar = self.menuBar()

        # Меню файл
        menuFile = menuBar.addMenu('File')
        menuFile.addAction('New Tab')
        menuFile.addAction('New Window')
        menuFile.addAction('Create new folder')
        menuFile.addAction('Create new document')
        menuFile.addSeparator()
        menuFile.addAction('Connect to Server...')
        menuFile.addSeparator()
        menuFile.addAction('Properties')
        menuFile.addAction('Close all windows')
        menuFile.addAction('Close')

        # Выход
        exitAction = menuFile.addAction('Exit')
        exitAction.triggered.connect(self.exit)
        exitAction.setShortcut(QKeySequence(KeyManager.getSequence(Sequence.Exit)))
        # 'Браузерное' сочетание
        exitDirectionAction = QAction(self)
        self.addAction(exitDirectionAction)
        exitDirectionAction.triggered.connect(self.exit)
        exitDirectionAction.setShortcut(QKeySequence(KeyManager.getSequence(Sequence.ExitDirect)))

        # Меню Edit
        menuEdit = menuBar.addMenu('Edit')
        menuEdit.addAction('Undo')
        menuEdit.addAction('Redo')
        menuEdit.addSeparator()
        menuEdit.addAction('Cut')
        menuEdit.addAction('Copy')
        menuEdit.addAction('Paste')
        menuEdit.addSeparator()
        menuEdit.addAction('Select All')
        menuEdit.addAction('Select item matching')
        menuEdit.addAction('Invert selection')
        menuEdit.addSeparator()
        menuEdit.addAction('Pin')
        menuEdit.addAction('Duplicate')
        menuEdit.addAction('Make links')
        menuEdit.addAction('Rename')
        menuEdit.addMenu('Copy to')
        menuEdit.addMenu('Move to')
        menuEdit.addSeparator()
        menuEdit.addAction('Move to trash')
        menuEdit.addAction('Delete')
        menuEdit.addSeparator()
        menuEdit.addAction('Compress...')
        menuEdit.addSeparator()
        menuEdit.addAction('Plugins')
        menuEdit.addAction('Preferences')

        # Меню View
        menuView = menuBar.addMenu('View')
        menuView.addAction('Reload')
        menuView.addSeparator()
        menuView.addMenu('Sidebar')
        # menuGo
        menuGo = menuBar.addMenu('Go')
        menuGo.addAction('Open parent')
        menuGo.addAction('Back')
        menuGo.addAction('Forward')
        menuGo.addAction('Same location for other pane')
        menuGo.addSeparator()
        menuGo.addAction('Home')
        menuGo.addAction('Computer')
        menuGo.addAction('Templates')
        menuGo.addAction('Trash')
        menuGo.addAction('Network')
        menuGo.addAction('Search for files...')

        # Меню Bookmarks
        menuBookmarks = menuBar.addMenu('Bookmarks')
        menuBookmarks.addAction('Add Bookmarsk')
        menuBookmarks.addAction('Edit Bookmarks...')
        menuBookmarks.addSeparator()

        # Меню помощь
        menuHelp = menuBar.addMenu('Help')
        menuHelp.addAction('All Topics')
        menuHelp.addAction('Keyboard shortcuts')
        menuHelp.addSeparator()
        aboutAction = menuHelp.addAction('About')
        aboutAction.triggered.connect(self.about)
        pass

    def toolBarGenerator(self):
        self.addToolBar(self.toolBar)
        toolBack = self.toolBar.addAction('Back')
        toolBack.triggered.connect(self.model.goBack)

        toolNext = self.toolBar.addAction('Next')
        toolNext.triggered.connect(self.model.goNext)
        toolUp = self.toolBar.addAction('Up')
        toolUp.triggered.connect(self.model.goUp)

        emptyLeft = QWidget()
        emptyLeft.setMaximumWidth(20)
        emptyLeft.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        #self.toolBar.addWidget(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.toolBar.addWidget(emptyLeft)
        self.pathLine = QLineEdit()
        self.pathLine.returnPressed.connect(self.insertPath)
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

    def insertPath(self):
        path = self.pathLine.text()
        print(path)
        self.model.setPath(path)
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
