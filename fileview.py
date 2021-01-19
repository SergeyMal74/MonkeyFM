

from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets

from filemodel import FileModel
from PyQt5.QtWidgets import QTableView

from PyQt5.QtWidgets import QAction, QToolBar, QFileSystemModel, QHeaderView, QAbstractItemView

import os, sys, subprocess

from PySide2.QtCore import Signal, Slot  

class FileView(QTableView):
    """
    Класс для отображения структуры каталога
    """
    def __init__(self):
        super().__init__()

        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.doubleClicked.connect(self.actionClicked)

        self.__model__ = self.model
        pass
    
    def actionClicked(self, index):
        row = index.row()
        self.__model__.actionItem(row)
        pass

    def setModel(self, model):
        self.__model__ = model
        QTableView.setModel(self, model)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        pass


