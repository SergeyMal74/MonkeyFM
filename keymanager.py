import sys
import random
from PyQt5 import QtGui, uic
from PyQt5 import QtWidgets
from enum import Enum

class Sequence(Enum):
    Exit = 1
    ExitDirect = 2
    CreateNewFolder = 3
    CreateNewFile = 4

SHORTCUT = {
    Sequence.Exit: 'Ctrl+Q', # Выход из приложения
    Sequence.ExitDirect: 'Ctrl+W',
    Sequence.CreateNewFolder: 'Ctrl+N', # Создать новую папку
    Sequence.CreateNewFile: 'Ctrl+Shift+N' # Создать новый файл
}

class KeyManager:
    """
    Класс для обработки нажатий клавиатуры
    """
    def __init__(self):
        pass

    def getSequence(sequence):
        """
        Возвращает символьное значение дефолтных сочетаний
        """
        return SHORTCUT[sequence]
        pass

