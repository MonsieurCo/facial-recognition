from typing import Optional

from PIL import Image
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPixmap, QMouseEvent, QScreen
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication


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

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.destination = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() & QtCore.Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            rect = QtWidgets.QGraphicsRectItem(rect)
            br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
            rect.setBrush(br)
            self.parent.addItem(rect)

            self.begin, self.destination = QPoint(), QPoint()

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
            im = im.resize((newWidth, newHeight))
            splitedFPath = self.fPath.split(".")
            self.fPath = splitedFPath[0] + "-resized" + "." + splitedFPath[1]
            im.save(self.fPath)
        self.resize(newWidth, newHeight)
        self.setFixedSize(self.size())
