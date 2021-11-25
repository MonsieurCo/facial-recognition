import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import QFileDialog, QMainWindow, QStatusBar, QLabel


class MenuBar(QMainWindow):
    def __init__(self, frame):
        super().__init__()

        #self.label = label
        self.frame=frame

        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open = QAction("Open", self)
        open.setShortcut("Ctrl+o")
        open.triggered.connect(self.loadFile)
        file_menu.addAction(open)

        save = QAction("Save", self)
        save.setShortcut("Ctrl+s")
        file_menu.addAction(save)

        close = QAction("Close", self)
        close.setShortcut("Ctrl+w")
        close.triggered.connect(self.closeImage)
        file_menu.addAction(close)

        file_menu.triggered[QAction].connect(self.processtrigger)

    def processtrigger(self, q):
        print(q.text() + " is triggered")

    def loadFile(self):
        self.fileName = QFileDialog.getOpenFileName(self)
        self.loadImage()

    def loadImage(self):
        fPath = self.fileName[0]
        if fPath != "":
            self.pixmap = QPixmap(fPath)
            self.label.setPixmap(self.pixmap)
            self.label.setFixedSize(self.size())

    def closeImage(self):
        if(self.frame!=None):
            self.frame.close()
