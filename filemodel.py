
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtCore import QAbstractTableModel, Qt

from abc import ABCMeta, abstractmethod, abstractproperty

import os
import sys
import time
import getpass
import subprocess

# Дефолтная директория - хомяк + текущий пользователь
defaultPath = '/home/user' #+ getpass.getuser()

# Отображаемые данные файла
headerName = ['Name', 'Size', 'Type', 'Date modified']

# Флаги для headerName
flags = ['name', 'size', 'type', 'mtime']

#####################################################
local = 0
ssh = 1

class Paginator:
    def __init__(self):
        self.statusList = ['local', 'ssh']
        self.status = local
        pass

    def directionalArrow(self, path):
        if(path.find('ssh:///') != -1):
            self.status = ssh
            return True
        else:
            self.status = local
            return False
        pass
    
    def listdir(self, path):
        if self.status == local:
            return os.listdir(path)
        elif self.status == ssh:
            return ['1', '2', '3']
        pass

    def getsize(self, path):
        if self.status == local:
            return os.path.getsize(path)
        elif self.status == ssh:
            return 500
        pass

    def isdir(self, path):
        if self.status == local:
            return os.path.isdir(path)
        elif self.status == ssh:
            return 500
        pass
    
    def isfile(self, path):
        if self.status == local:
            return os.path.isfile(path)
        elif self.status == ssh:
            return 500
        pass

    def islink(self, path):
        if self.status == local:
            return os.path.islink(path)
        elif self.status == ssh:
            return 500
        pass
    
    def getmtime(self, path):
        if self.status == local:
            return os.path.getmtime(path)
        elif self.status == ssh:
            return 500
        pass
    
    def basename(self, path):
        if self.status == local:
            return os.path.basename(path)
        elif self.status == ssh:
            return 500
        pass
    
    def startfile(self, path):
        if self.status == local:
            os.startfile(path)
        elif self.status == ssh:
            pass
        pass


class FileModel(QAbstractTableModel):
    """
    Абстрактный класс файловой модели
    """
    def __init__(self):
        super().__init__()
        self.paginator = Paginator()

        self.__fileLayer__ = list()
        self.__pathHistory__ = list()
        self.__nextPath__ = list()
        self.__currentPath__ = str()

        self.setPath(defaultPath)
        pass

    def setPath(self, path):
        """
        Метод наполнения модели при изменении пути
        """
        # Заполнение содержимым
        self.beginResetModel()
        self.filling(path)
        self.endResetModel()
        pass

    def filling(self, path=None):
        """
        Заполнение модели содержимым
        """
        # Если принимаемый путь пустой, значит используем дефолтный
        if path == None:
                path = defaultPath
        elif self.paginator.directionalArrow(path):
            pass

        # Получаем список содержимого
        fileList = self.paginator.listdir(path)
        # Сортируем по алфавиту
        fileList.sort()

        # Кортеж для данных по файлам
        self.__fileLayer__.clear()
        for it in fileList:
            data_line = []

            # Полный путь к файлу/директории
            self.fullPath = path + '/' + it
            
            # Добавление имени в конец
            data_line.append(it)

            # Размер файла
            byteSize = self.paginator.getsize(self.fullPath)
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
            if self.paginator.isdir(self.fullPath):
                data_line.append('Directory')
            elif self.paginator.isfile(self.fullPath):
                data_line.append('File')
            elif self.paginator.islink(self.fullPath):
                data_line.append('Symlink')
            else:
                data_line.append('None')

            # Дата модификации
            data_line.append(time.ctime(self.paginator.getmtime(self.fullPath)))
            self.__fileLayer__.append(data_line)

            # Присваиваем текущий путь хранимой переменной
            self.__currentPath__ = path
        pass

    def rowCount(self, index=QtCore.QModelIndex()):
        if index.isValid():
            return index.internalPointer().columnCount()
        return len(self.__fileLayer__)

    def columnCount(self, index=QtCore.QModelIndex()):
        if index.isValid():
            return index.internalPointer().columnCount()
        return 4

    def data(self, index, role):
        column = index.column()
        row = index.row()

        if row >= len(self.__fileLayer__):
            return None

        it = self.__fileLayer__[row]

        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return it[column]
        return None

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

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

    def actionItem(self, row):
        fileName = self.__fileLayer__[row][0]

        fullPath = self.__currentPath__ + '/' + fileName
        if self.paginator.isfile(fullPath):
            self.open_file(fullPath)
        elif self.paginator.isdir(fullPath):
            self.__pathHistory__.append(self.__currentPath__)
            self.setPath(fullPath)
        pass

    def goUp(self):
        """
        Перейти во верхнюю дерикторию
        """
        self.__pathHistory__.append(self.__currentPath__)
        
        basename = self.paginator.basename(self.__currentPath__)
        lnum = self.__currentPath__.rfind(basename)
        newPath = self.__currentPath__
        if lnum > -1:
            newPath = self.__currentPath__[:lnum]
            if len(newPath) > 1 and newPath[len(newPath)-1] == '/':
                newPath = newPath[:len(newPath)-1]
        self.setPath(newPath)
        pass

    def goNext(self):
        if len(self.__nextPath__) == 0:
            print('Next path is empty')
        else:
            lastPath = self.__nextPath__.pop()
            self.__pathHistory__.append(self.__currentPath__)
            self.setPath(lastPath)
        pass

    def goBack(self):
        if len(self.__pathHistory__) == 0:
            print('Last path is empty')
        else:
            lastPath = self.__pathHistory__.pop()
            self.__nextPath__.append(self.__currentPath__)
            self.setPath(lastPath)
        pass

    def open_file(self, filename):
        """
        Открытие итема
        """
        # Если винда, открыть через функции win32
        if sys.platform == "win32":
            self.paginator.startfile(filename)
        # Если нет, запустить подпроцесс
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])