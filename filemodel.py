
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtCore import QAbstractTableModel, Qt

from abc import ABCMeta, abstractmethod, abstractproperty

import os
import time
import getpass

# Дефолтная директория - хомяк + текущий пользователь
defaultPath = '/home/' + getpass.getuser()

# Отображаемые данные файла
headerName = ['Name', 'Size', 'Type', 'Date modified']

# Флаги для headerName
flags = ['name', 'size', 'type', 'mtime']

class FileModel(QAbstractTableModel):
    """
    Абстрактный класс файловой модели
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.fileLayer = []
        self.filling()
        

        # Переменная для хранения пути текущей дериктории
        self.currentPath = defaultPath
        pass

    def setPath(self, path):
        """
        Метод наполнения модели при изменении пути
        """

        # Заполнение содержимым
        self.beginResetModel()
        self.filling(path)
        self.endResetModel()

        # Сброс оторажения
        self.parent.reset()
        self.parent.scrollToTop()
        pass

    def filling(self, path=None):
        """
        Заполнение модели содержимым
        """
        # Если принимаемый путь пустой, значит используем дефолтный
        if path == None:
                path = defaultPath

        # Получаем список содержимого
        fileList = os.listdir(path)
        # Сортируем по алфавиту
        fileList.sort()

        # Кортеж для данных по файлам
        self.fileLayer.clear()
        for it in fileList:
            data_line = []

            # Полный путь к файлу/директории
            self.fullPath = path + '/' + it
            
            # Добавление имени в конец
            data_line.append(it)

            # Размер файла
            byteSize = os.path.getsize(self.fullPath)
            # Tb Gb Mb Kb b
            kb_t = int(byteSize/1024)
            b_t = byteSize-(kb_t*1024)
            mb_t = int(kb_t/1024)
            kb_t = kb_t-(mb_t*1024)
            gb_t = int(mb_t/1024)
            mb_t = mb_t-(gb_t*1024)
            tb_t = int(gb_t/1024)
            
            size_str = ''
            if tb_t > 0:
                size_str = str(tb_t+1) + ' Tb'
            elif gb_t > 0:
                size_str = str(gb_t+1) + ' Gb'
            elif mb_t > 0:
                size_str = str(mb_t+1) + ' Mb'
            elif kb_t > 0:
                size_str = str(kb_t+1) + ' Kb'
            elif b_t > 0:
                size_str = str(b_t) + ' b'
            else:
                size_str = ''

            data_line.append(size_str)

            # Обработка пути - присваивание типа
            if os.path.isdir(self.fullPath):
                data_line.append('Directory')
            elif os.path.isfile(self.fullPath):
                data_line.append('File')
            elif os.path.islink(self.fullPath):
                data_line.append('Symlink')
            else:
                data_line.append('None')

            # Дата модификации
            data_line.append(time.ctime(os.path.getmtime(self.fullPath)))
            self.fileLayer.append(data_line)

            # Присваиваем текущий путь хранимой переменной
            self.currentPath = path
        pass

    def rowCount(self, index=QtCore.QModelIndex()):
        if index.isValid():
            return index.internalPointer().columnCount()
        #print("fileLayer = ", len(self.fileLayer))
        return len(self.fileLayer)

    def columnCount(self, index=QtCore.QModelIndex()):
        if index.isValid():
            return index.internalPointer().columnCount()
        return 4

    def data(self, index, role):
        column = index.column()
        row = index.row()

        if row >= len(self.fileLayer):
            return None

        it = self.fileLayer[row]

        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return it[column]
        return None

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def getCaracter(self, row, flag):
        it = self.fileLayer[row]
        if flag == 'name':
            return it[0]
        elif flag == 'size':
            return it[1]
        elif flag == 'type':
            return it[2]
        elif flag == 'mtime':
            return it[3]
        return None        

    def headerData(self, section, orientation, role):
        """
        Заголовок
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return headerName[section]
        else:
            return section+1
        pass

    def getCurrentPath(self):
        """
        Возврат текущей директории
        """
        return self.currentPath