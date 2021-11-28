from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QVBoxLayout

from src.widgets.FrameImageWidget import FrameImage


class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, bopen, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__()

        self.parent = parent
        self.frame = parent.frame

        self.fileMenu = self.addMenu("File")
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)

        if bopen:
            self.open = self.fileMenu.addMenu("Open")

            self.openFile = QAction("Open file", self)
            self.openFile.setShortcut("Ctrl+o")
            self.openFile.triggered.connect(self.loadFile)
            self.open.addAction(self.openFile)

            self.openFold = QAction("Open folder", self)
            self.openFold.setShortcut("Ctrl+Shift+O")
            self.openFold.triggered.connect(self.frame.load)
            self.open.addAction(self.openFold)

        self.save = QAction("Save", self)
        self.save.setShortcut("Ctrl+s")
        self.fileMenu.addAction(self.save)

        self.close = QAction("Close", self)
        self.close.setShortcut("Ctrl+w")
        self.close.triggered.connect(self.closeImage)
        self.fileMenu.addAction(self.close)

        self.fileMenu.triggered[QAction].connect(self.processTrigger)

        self.layout.addWidget(self.fileMenu)
        self.setLayout(self.layout)

        self.fileName = None

    def processTrigger(self, q):
        print(q.text() + " is triggered")

    def loadFile(self):
        self.fileName = QFileDialog.getOpenFileName(self)
        self.loadImage()

    def loadImage(self):
        fPath = self.fileName[0]
        if fPath != "":
            self.newFrame = FrameImage(fPath, "test", None)
            self.newFrame.show()

    def closeImage(self):
        if self.parent is not None:
            self.parent.close()
