import time
from typing import Optional

from PIL import Image
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPixmap, QMouseEvent, QScreen
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication

from src.widgets.CategorieFrameWidget import CategorieFrame


class View(QGraphicsView):
    def __init__(self, fPath: str, parent: Optional[QGraphicsScene] = ...) -> None:
        super().__init__(parent)
        self.fPath = fPath
        self.parent = parent
        self.start = QPoint()
        self.begin = QtCore.QPoint()
        self.destination = QtCore.QPoint()
        self.setupImage()
        self.pixmap = QPixmap(self.fPath)
        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.parent.addItem(self.pixmapItem)
        self.currentRect = None
        self.frame = None

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self._update(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._update(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() & QtCore.Qt.LeftButton:
            self.parent.removeItem(self.currentRect)
            self.parent.addItem(QtWidgets.QGraphicsRectItem(QRect(self.begin, self.destination).normalized()))
            self.begin, self.destination = QPoint(), QPoint()
            self.frame = CategorieFrame(None)
            self.frame.show()
            self.frame.setFocus()


    def _update(self, event: QMouseEvent):
        if self.currentRect is not None:
            self.parent.removeItem(self.currentRect)
        self.currentRect = QtWidgets.QGraphicsRectItem(QRect(self.begin, self.destination).normalized())
        self.destination = event.pos()
        self.parent.addItem(self.currentRect)

    def setupImage(self):
        resize = False
        im: Image = Image.open(self.fPath)
        primaryScreenSize = QScreen.availableGeometry(QApplication.primaryScreen())

        width, height = primaryScreenSize.width(), primaryScreenSize.height()
        newWidth, newHeight = im.size
        if newWidth > width or newHeight > height:
            resize = True

        newWidth = min(newWidth, width)
        newHeight = min(newHeight, height)
        if resize:
            newWidth -= 20
            newHeight -= 70
            im = im.resize((newWidth, newHeight))
            splitFPath = self.fPath.split(".")
            self.fPath = splitFPath[0] + "-resized" + "." + splitFPath[1]
            im.save(self.fPath)
        self.resize(newWidth, newHeight)
        self.setFixedSize(self.size())
