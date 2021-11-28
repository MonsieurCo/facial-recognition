from typing import Optional

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QRect
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QGraphicsScene, QApplication
from PySide6.QtWidgets import QVBoxLayout

from src import MenuBarWidget
from src import SelectAreaGraphicSceneWidget


class FrameImage(QtWidgets.QWidget):
    def __init__(self, fPath, name, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.frame = None
        self.title = name
        self.setWindowTitle(self.title)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.graphicsView = None
        self.scene = QGraphicsScene(self)
        self.menu = MenuBarWidget.MenuBar(False, self)
        self.layout.setMenuBar(self.menu)

        self.fPath = fPath
        self.name = name
        self.load()

    def load(self):
        if self.graphicsView is not None:
            self.scene.removeItem(self.graphicsView)
        if self.fPath != "":
            self.graphicsView = SelectAreaGraphicSceneWidget.View(self.fPath, self.scene)
            self.scene.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
            self.layout.addWidget(self.graphicsView, alignment=QtCore.Qt.AlignCenter)
            # center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
            # geo = self.frameGeometry()
            # geo.moveCenter(center)
            # self.move(geo.topLeft())
            self.setLayout(self.layout)
