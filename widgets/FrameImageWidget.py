from typing import Optional

import qdarkstyle
from PySide6 import QtWidgets
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout

from widgets import SelectAreaGraphicSceneWidget
from widgets import MenuBarWidget


class FrameImage(QtWidgets.QWidget):
    def __init__(self, fPath, name, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.frame = self

        self.title = name
        self.setWindowTitle(self.title)
        self.resize(1280, 720)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.graphicsView = None
        self.scene = QGraphicsScene(self)

        self.menu = MenuBarWidget.MenuBar(False, self)
        self.layout.addWidget(self.menu)

        self.fPath = fPath
        self.name = name
        self.load()

    def load(self):
        self.scene.removeItem(self.graphicsView)
        if self.fPath != "":
            self.graphicsView = SelectAreaGraphicSceneWidget.View(self.fPath, self.scene)
            self.layout.addWidget(self.graphicsView)
            self.setLayout(self.layout)
