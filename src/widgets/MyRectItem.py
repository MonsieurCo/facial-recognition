from typing import Optional

import PySide6
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QGraphicsRectItem

from src import AnnotateManager
from src.widgets import CategorieFrameWidget, rects


class MyRect(QGraphicsRectItem):
    def __init__(self, fPath: str, brush: QtGui.QBrush, size, choice: str, scene,
                 parent: Optional[PySide6.QtWidgets.QGraphicsItem] = ...) -> None:
        super().__init__(parent)
        self.normalized = self.rect().normalized()
        self.fPath = fPath
        self.parent = parent
        self.size = size
        self.choice = choice
        self.setBrush(brush)
        self.setOpacity(0.25)
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        self.scene = scene

    def mouseDoubleClickEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)
        self.frame = CategorieFrameWidget.CategorieFrame(self.fPath,
                                                         self.normalized.topLeft(),
                                                         self.normalized.bottomRight(),
                                                         self,
                                                         self.size,
                                                         self.parent,
                                                         True)
        self.frame.show()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.buttons() & QtCore.Qt.RightButton:
            self.Xbegin = self.normalized.topLeft().x()
            self.Ybegin = self.normalized.topLeft().y()
            AnnotateManager.deleteAnnotationByCoord(self.Xbegin, self.Ybegin)
            self.scene.removeItem(self)
