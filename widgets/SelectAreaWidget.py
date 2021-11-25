from typing import Optional

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QMouseEvent, QPainter, QPixmap


class SelectAreaWidget(QtWidgets.QWidget):

    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self.begin = QtCore.QPoint()
        self.destination = QtCore.QPoint()
        self.pix = QPixmap(self.rect().size())
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

    def paintEvent(self, event: QMouseEvent):
        painter = QPainter(self)
        painter.drawPixmap(QtCore.QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull():
            rect = QtCore.QRect(self.begin, self.destination)
            painter.drawRect(rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.destination = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() & QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.destination = event.pos()
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self)
            painter.drawRect(rect)
            self.begin, self.begin = QPoint(), QPoint()
            self.update()
