from typing import Optional

import PySide6.QtGui
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout

from src import AnnotateManager
from src.QtColors import QtColors
from src.widgets import SelectAreaGraphicSceneWidget, MenuBarWidget
from src.widgets import rects
from src.widgets.SelectAreaGraphicSceneWidget import MyRect


class FrameImage(QtWidgets.QWidget):
    def __init__(self, fPath, name, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.frame = None
        self.title = name
        self.setWindowTitle(self.title)

        #     Categories PATH
        self.fpathCSV = ""
        self.fpathJSON = ""
        self.isJSON = True

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.graphicsView = None
        self.scene = QGraphicsScene(self)
        self.menu = MenuBarWidget.MenuBar(False, self)
        self.layout.setMenuBar(self.menu)

        self.fPath = fPath
        self.name = name
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        self.load()
        self.show()

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

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        super().showEvent(event)
        try:
            annotations = AnnotateManager.annotations[self.fName]["annotations"]

            if self.fName not in rects.RECTS:
                rects.RECTS[self.fName] = []
            for annotation in annotations:
                rect = MyRect(self.fPath,
                              QtGui.QBrush(QtColors.COLORS[annotation["categorie_id"] % QtColors.lengthColors]),
                              (self.scene.width(), self.scene.height()),
                              "",
                              QRect(
                                  QPoint(annotation["coords"]["beginX"],
                                         annotation["coords"]["beginY"]),
                                  QPoint(
                                      annotation["coords"]["destinationX"],
                                      annotation["coords"]["destinationY"]
                                  )).normalized())

                rects.RECTS[self.fName].append(rect)
                self.scene.addItem(rect)

            for rect in rects.RECTS[self.fName]:
                self.scene.addItem(rect)

        except Exception as e:
            pass

    def getScene(self) -> QGraphicsScene:
        return self.scene

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        super().closeEvent(event)
        # rects.RECTS[self.fName] = []
        # for item in self.scene.items():
        #     if isinstance(item, QGraphicsRectItem):
        #         rects.RECTS[self.fName].append(item)
        #         print(item)

    #     FrameImageMemoize.FRAME_IMAGES[self.fName] = self

    # def getRects(self):
    #     return self.rects
