from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *

#from PyQt5.QtWidgets import QAbstractItemModel
from PyQt5.QtCore import QVariant, QAbstractItemModel


class Node(object):
    def __init__(self, name, parent=None,checked=False):

        self.name = (name)
        #self.state = (state)
        #self.description = (description)
        #self.otro = (otro)

        self.parent = parent
        self.children = []

        self.setParent(parent)

    def setParent(self, parent):
        if parent != None:
            self.parent = parent
            self.parent.appendChild(self)
        else:
            self.parent = None

    def appendChild(self, child):
        self.children.append(child)

    def childAtRow(self, row):
        return self.children[row]

    def rowOfChild(self, child):       
        for i, item in enumerate(self.children):
            if item == child:
                return i
        return -1

    def removeChild(self, row):
        value = self.children[row]
        self.children.remove(value)

        return True

    def __len__(self):
        return len(self.children)

class PlaceModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(PlaceModel, self).__init__(parent)       
        self.treeView = parent

        self.columns = 1
        self.headers = ['Directorio']

        # Create items
        self.root = Node('Places', None)
        # Computer places
        computer = Node('My Computer', self.root)
        home = Node('Home', computer)
        desktop = Node('Desktop', computer)
        documents = Node('Documents', computer)

        itemB = Node('Bookmarks', self.root)       
        itemC = Node('Devices', self.root)
        itemD = Node('Network', self.root)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section])
        return QVariant()

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable| Qt.ItemIsUserCheckable

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()

        return True

    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        return self.createIndex(row, column, node.childAtRow(row))

    def data(self, index, role):

        if role != Qt.DisplayRole:
            return QVariant()

        if not index.isValid():
            return None

        node = self.nodeFromIndex(index)

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return QVariant(node.name)
        if role == Qt.CheckStateRole:
            if node.checked():
                return Qt.Checked
            else:
                return Qt.Unchecked

        if index.column() == 1:
            return QVariant(node.state)

        elif index.column() == 2:
            return QVariant(node.description)

        elif index.column() == 3:
            return QVariant(node.otro)

        else:
            return QVariant()

    def setData(self, index, value, role=Qt.EditRole):

        if index.isValid():
            if role == Qt.CheckStateRole:
                node = index.internalPointer()
                node.setChecked(not node.checked())
                return True
        return False

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()

        node = self.nodeFromIndex(child)

        if node is None:
            return QModelIndex()

        parent = node.parent

        if parent is None:
            return QModelIndex()

        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)

        assert row != - 1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.root