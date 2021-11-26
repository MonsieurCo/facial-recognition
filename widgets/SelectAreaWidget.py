import random
from typing import Optional

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPoint, QRect, QSize
from PySide6.QtGui import QMouseEvent, QPainter, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene


class SelectAreaWidget(QtWidgets.QWidget):

    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self.parent = parent
        self.start = QPoint()
        self.begin = QtCore.QPoint()
        self.destination = QtCore.QPoint()
        self.pix = QPixmap(QSize(0, 0))
        self.rects = []

    def paintEvent(self, event: QMouseEvent):
        painter = QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        painter.setBrush(br)
        painter.drawPixmap(QtCore.QPoint(), self.pix)
        painter.setPen(QtCore.Qt.red)

        if not self.begin.isNull() and not self.destination.isNull():
            rect = QtCore.QRect(self.begin, self.destination)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.start = event.pos()
            self.begin = event.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            print("POINT 2")
            self.destination = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() & QtCore.Qt.LeftButton:
            self.destination = event.pos()
            rect = QRect(self.start, self.destination)
            self.rects.append(rect)
            self.update()

            self.begin, self.destination, self.start = QPoint(), QPoint(), QPoint()
            # painter.end()


