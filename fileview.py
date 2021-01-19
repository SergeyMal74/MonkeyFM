

from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets

from filemodel import FileModel
from PyQt5.QtWidgets import QTableView

from PyQt5.QtWidgets import QAction, QToolBar, QFileSystemModel, QHeaderView, QAbstractItemView
from PyQt5.QtCore import QDir, pyqtSignal, QObject

import os, sys, subprocess

import getpass

# Дефолтная директория - хомяк + текущий пользователь
defaultPath = '/home/' + getpass.getuser()

class Communicate(QObject):
    """
    Сигналы FileView
    """
    changePath = pyqtSignal([str]) # Путь изменился

class FileViewSignals(QObject):
    """
    Класс с сигналами FileView
    
    Нужен для доступа к сигналам класса чужими классами

    """
    c = Communicate()

class FileView(QTableView):
    """
    Класс для отображения структуры каталога
    """
    def __init__(self):
        super().__init__()

        self.c = FileViewSignals.c

        self.model = FileModel(self)
        self.setModel(self.model)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.doubleClicked.connect(self.actionItem)

        # history
        self.pathHistory = []
        self.nextPath = []

        self.model.setPath(defaultPath)
        self.c.changePath.emit(defaultPath)
        pass

    def actionItem(self, index):
        row = index.row()
        currentPath = self.model.getCurrentPath()
        fileName = self.model.getCaracter(row, 'name')

        fullPath = currentPath + '/' + fileName
        if os.path.isfile(fullPath):
            self.open_file(fullPath)
        elif os.path.isdir(fullPath):
            self.pathHistory.append(self.model.getCurrentPath())
            self.model.setPath(fullPath)
            self.c.changePath.emit(fullPath)
        pass

    def goUp(self):
        """
        Перейти во верхнюю дерикторию
        """
        currentPath = self.model.getCurrentPath()
        self.pathHistory.append(currentPath)

        basename = os.path.basename(currentPath)
        lnum = currentPath.rfind(basename)
        newPath = currentPath
        if lnum > -1:
            newPath = currentPath[:lnum]
            if len(newPath) > 1 and newPath[len(newPath)-1] == '/':
                newPath = newPath[:len(newPath)-1]
        self.model.setPath(newPath)
        self.c.changePath.emit(newPath)
        pass

    def goNext(self):
        if len(self.nextPath) == 0:
            print('Next path is empty')
        else:
            lastPath = self.nextPath.pop()
            self.pathHistory.append(self.model.getCurrentPath())
            self.model.setPath(lastPath)
            self.c.changePath.emit(lastPath)
        pass

    def goBack(self):
        if len(self.pathHistory) == 0:
            print('Last path is empty')
        else:
            lastPath = self.pathHistory.pop()
            self.nextPath.append(self.model.getCurrentPath())
            self.model.setPath(lastPath)
            self.c.changePath.emit(lastPath)
        pass

    def getCurrentFolder(self):
        """
        Возвращает название текущего каталога (не путь)
        """
        currentPath = self.model.getCurrentPath()
        return os.path.dirname(currentPath)
    
    def getCurrentPath(self):
        """
        Возвращает путь текущего каталога
        """
        return self.model.getCurrentPath()

    def open_file(self, filename):
        """
        Открытие итема
        """
        # Если винда, открыть через функции win32
        if sys.platform == "win32":
            os.startfile(filename)
        # Если нет, запустить подпроцесс
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

