import sys
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGridLayout, QLabel, QVBoxLayout, QApplication, QFrame
from typing import Optional

from widgets import SelectAreaWidget, MenuBar

class FrameImage(QtWidgets.QWidget):
    def __init__(self, path, name, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self.title = name
        self.setWindowTitle(self.title)
        # self.setFixedSize(QSize(1280, 720))
        self.resize(1280, 720)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)

        self.label = QLabel(self)

        self.path = path
        self.name = name
        loadImage(self, path)
        self.layout.addWidget(SelectAreaWidget(self))

        #self.show()

def loadFile(self, path):
    self.fileName = QFileDialog.getOpenFileName(self)
    self.loadImage(path)


def loadImage(self, fPath):
    #fPath = self.fileName[0]
    if fPath != "":
        # for i in reversed(range(self.layout.count())):
        #     self.layout.itemAt(i).widget().setParent(None)
        # self.layout.
        self.pixmap = QPixmap(fPath)
        self.label.setPixmap(self.pixmap)
        self.label.setFixedSize(self.size())
