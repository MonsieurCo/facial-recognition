from typing import Optional

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene


class View(QGraphicsView):
    def __init__(self, fPath: str, parent: Optional[QGraphicsScene] = ...) -> None:
        super().__init__(parent)
        self.fPath = fPath
        self.parent = parent
        self.start = QPoint()
        self.begin = QtCore.QPoint()
        self.destination = QtCore.QPoint()
        self.pixmap = QPixmap(self.fPath)
        self.setFixedSize(1280, 720)

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

