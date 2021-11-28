from typing import Optional

import qdarkstyle
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QSize, QRectF, QRect
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QGraphicsScene, QApplication
from PySide6.QtWidgets import QVBoxLayout
from PySide6 import QtGui

from widgets import SelectAreaGraphicSceneWidget
from widgets import MenuBarWidget
import ctypes




class FrameImage(QtWidgets.QWidget):
    def __init__(self, fPath, name, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.frame = self

        self.title = name
        self.setWindowTitle(self.title)


        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.graphicsView = None
        self.scene = QGraphicsScene(self)
        self.layout.setMenuBar(MenuBarWidget.MenuBar(False, self))

        self.fPath = fPath
        self.name = name
        self.load()

    def load(self):
        if self.graphicsView is not None:
            self.scene.removeItem(self.graphicsView)
        if self.fPath != "":
            self.graphicsView = SelectAreaGraphicSceneWidget.View(self.fPath, self.scene)
            self.resize(self.graphicsView.size())
            self.scene.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
            self.layout.addWidget(self.graphicsView)
            self.setLayout(self.layout)
