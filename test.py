from typing import Optional

import PySide6.QtWidgets
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QMouseEvent, QPixmap, QPen
from PySide6.QtWidgets import QGraphicsView, QMainWindow, QGraphicsScene, QApplication


class View(QGraphicsView):

    def __init__(self, parent: Optional[QGraphicsScene] = ...) -> None:
        super().__init__(parent)
        self.parent = parent
        self.start = QPoint()
        self.begin = QtCore.QPoint()
        self.destination = QtCore.QPoint()
        self.setFixedSize(1280, 720)

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        super().paintEvent(event)

        rect = QRect(self.begin, self.destination)
        rect = QtWidgets.QGraphicsRectItem(rect)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        rect.setPen(QPen(QtCore.Qt.red))
        rect.setBrush(br)

        # if not self.begin.isNull() and not self.destination.isNull():
        #     rect = QtCore.QRect(self.begin, self.destination)
        #     painter.drawRect(rect.normalized())

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            print("POINT 1")

            self.start = event.pos()
            self.begin = event.pos()
            self.destination = self.begin

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            print("POINT 2")
            self.destination = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() & QtCore.Qt.LeftButton:
            print("POINT 3")
            self.destination = event.pos()

            rect = QRect(self.begin, self.destination)
            rect = QtWidgets.QGraphicsRectItem(rect)
            br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
            rect.setBrush(br)
            self.parent.addItem(rect)
            self.begin, self.destination, self.start = QPoint(), QPoint(), QPoint()
            # painter.end()


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.s = QGraphicsScene(self)
        self.pixmap = QPixmap("assets/test.jpg")

        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.s.addItem(self.pixmapItem)
        self.v = View(self.s)
        self.View()
        self.resize(1280, 720)

    def mousePressEvent(self, event):
        print("QMainWindow mousePress")

    def mouseMoveEvent(self, event):
        print("QMainWindow mouseMove")

    def mouseReleaseEvent(self, event):
        print("QMainWindow mouseRelease")

    def View(self):
        self.setCentralWidget(self.v)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
