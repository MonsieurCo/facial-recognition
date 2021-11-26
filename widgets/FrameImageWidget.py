from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout

from widgets import SelectAreaGraphicSceneWidget


class FrameImage(QtWidgets.QWidget):
    def __init__(self, fPath, name, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.title = name
        self.setWindowTitle(self.title)
        self.resize(1280, 720)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.graphicsView = None
        self.scene = QGraphicsScene(self)

        self.fPath = fPath
        self.name = name
        self.loadImage()

    def loadImage(self):
        if self.fPath != "":
            self.graphicsView = SelectAreaGraphicSceneWidget.View(self.fPath, self.scene)
            self.layout.addWidget(self.graphicsView)
            self.setLayout(self.layout)
