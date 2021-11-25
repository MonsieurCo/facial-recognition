import sys

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGraphicsView, QMainWindow, QApplication, QLabel, QVBoxLayout
from PySide6.QtWidgets import QFileDialog, QGridLayout, QLabel, QVBoxLayout
from typing import Optional

from widgets.ImageButton import ImageButton


class MultiView(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.button = QtWidgets.QPushButton("Load folder")
        self.button.clicked.connect(self.loadFiles)
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.gridButtons: QGridLayout = QtWidgets.QGridLayout(self)
        self.gridButtons.setColumnMinimumWidth(4, 4)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.gridButtons)
        self.layout.addWidget(self.button)

    @QtCore.Slot()
    def loadFiles(self):
        for i in reversed(range(self.gridButtons.count())):
            self.gridButtons.itemAt(i).widget().setParent(None)
        dir_path = QFileDialog.getExistingDirectory(self)
        dir = QDir(dir_path)
        filter = ["*.png", "*.xpm", "*.jpg"]
        dir.setNameFilters(filter)
        pathsList = [QDir.filePath(dir, x) for x in dir.entryList()]
        self.buttons=[]
        for i in range(len(pathsList)):
            name = dir.entryList()[i]
            path = pathsList[i]
            tempButton = ImageButton(name, path, i, self)
            self.buttons.append(tempButton)
            self.gridButtons.addWidget(tempButton)
