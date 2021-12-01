from typing import Optional

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout

from src.widgets import SelectAreaGraphicSceneWidget, MenuBarWidget


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
        self.rects = []

        self.fPath = fPath
        self.name = name
        self.load()

    def load(self):
        if self.graphicsView is not None:
            self.scene.removeItem(self.graphicsView)
        if self.fPath != "":
            self.graphicsView = SelectAreaGraphicSceneWidget.View(self.fPath, self)
            print(self.graphicsView)
            self.scene.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
            self.layout.addWidget(self.graphicsView, alignment=QtCore.Qt.AlignCenter)
            # center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
            # geo = self.frameGeometry()
            # geo.moveCenter(center)
            # self.move(geo.topLeft())
            self.setLayout(self.layout)

    def mouseDoubleClickEvent(self, event):
        widget = self.childAt(event.pos())
        print("double click")
        if widget is not None and widget.objectName():
            print('dblclick:', widget.objectName())

    def getScene(self) -> QGraphicsScene:
        return self.scene

    def getRects(self):
        return self.rects
