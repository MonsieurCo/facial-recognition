import sys, random
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGraphicsView, QGridLayout, QMainWindow, QApplication, QLabel, QVBoxLayout
from typing import Optional

class MultiView(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)


        self.button = QtWidgets.QPushButton("Load folder")
        self.button.clicked.connect(self.loadFiles)
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.gridButtons : QVBoxLayout = QtWidgets.QVBoxLayout(self)
        #self.gridButtons.setColumnMinimumWidth(4,4)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.gridButtons)
        self.layout.addWidget(self.button)


    @QtCore.Slot()
    def loadFiles(self):
        dir_path = QFileDialog.getExistingDirectory(self)
        dir = QDir(dir_path)
        filter = ["*.png", "*.xpm", "*.jpg"]
        dir.setNameFilters(filter)
        pathsList = [QDir.filePath(dir, x) for x in dir.entryList()]
        print(pathsList)

        for i in range(len(pathsList)):
            tempbutton = QtWidgets.QPushButton(f"Image : {dir.entryList()[i]}")
            tempbutton.setFixedSize(70,70)
            #tempbutton.clicked.connect(self.openFile(pathsList[i]))
            self.gridButtons.addWidget(tempbutton)

    def openFile(self,path):
        pixmap = QPixmap(path)
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(self.size())