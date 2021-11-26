from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QVBoxLayout

from widgets.FrameImageWidget import FrameImage


class MenuBar(QtWidgets.QMenuBar):

    def __init__(self) -> None:
        super().__init__()

        self.fileMenu = self.addMenu("File")
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)

        self.open = QAction("Open", self)
        self.open.setShortcut("Ctrl+o")
        self.open.triggered.connect(self.loadFile)
        self.fileMenu.addAction(self.open)

        self.save = QAction("Save", self)
        self.save.setShortcut("Ctrl+s")
        self.fileMenu.addAction(self.save)

        self.close = QAction("Close", self)
        self.close.setShortcut("Ctrl+w")
        self.close.triggered.connect(self.closeImage)
        self.fileMenu.addAction(self.close)

        self.fileMenu.triggered[QAction].connect(self.processTrigger)
        self.frame = None
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
            self.frame = FrameImage(fPath, "test", None)
            self.frame.show()

    def closeImage(self):
        self.close()
