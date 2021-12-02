from typing import Optional

import PySide6
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QPoint, QRect
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout

from src import AnnotateManager, RECTS
from src.widgets import SelectAreaGraphicSceneWidget, MenuBarWidget, CategorieFrameWidget


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
        # self.rects: list[QGraphicsRectItem] = []

        self.fPath = fPath
        self.name = name
        self.load()

    def load(self):
        if self.graphicsView is not None:
            self.scene.removeItem(self.graphicsView)
        if self.fPath != "":
            self.graphicsView = SelectAreaGraphicSceneWidget.View(self.fPath,
                                                                  parent=self)
            self.scene.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
            self.layout.addWidget(self.graphicsView, alignment=QtCore.Qt.AlignCenter)
            # center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
            # geo = self.frameGeometry()
            # geo.moveCenter(center)
            # self.move(geo.topLeft())
            self.setLayout(self.layout)
            print("loaded")

    def mouseDoubleClickEvent(self, event):
        for rect in RECTS:
            normalizedRect = rect.rect().normalized()
            if normalizedRect.contains(event.pos()):
                self.frame = CategorieFrameWidget.CategorieFrame(self.fPath,
                                                                 normalizedRect.topLeft(),
                                                                 normalizedRect.bottomRight(),
                                                                 rect,
                                                                 self,
                                                                 True)
                self.frame.show()

    def showEvent(self, event: PySide6.QtGui.QShowEvent) -> None:
        try:
            annotations = AnnotateManager.annotations[self.fPath.split("/")[-1].split(".")[0]]["annotations"]
            for i, annotation in enumerate(annotations):
                rect = QtWidgets.QGraphicsRectItem(QRect(
                    QPoint(annotation["coords"]["beginX"],
                           annotation["coords"]["beginY"]),
                    QPoint(
                        annotation["coords"]["destinationX"],
                        annotation["coords"]["destinationY"]
                    )).normalized())
                self.scene.addItem(rect)
        except:
            pass

    def getScene(self) -> QGraphicsScene:
        return self.scene

    # def getRects(self):
    #     return self.rects
