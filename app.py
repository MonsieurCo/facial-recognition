import sys

import PySide6.QtGui
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QPoint, QSize, QRect
from PySide6.QtGui import QPixmap, QPainter, QMouseEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, \
    QWidget, QGraphicsScene

from widgets import SelectAreaGraphicScene

class ImageAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageAnnotator")
        # self.setFixedSize(QSize(1280, 720))
        self.resize(1280, 720)
        # self.loadImage()

        self.button = QtWidgets.QPushButton("Load files")
        self.button.clicked.connect(self.loadFile)

        self.label = QLabel(self)
        self._layout: QVBoxLayout = QVBoxLayout(self)

        self.fileName = None
        self.begin, self.destination = QPoint(), QPoint()


        self._layout.addWidget(self.button)

        self.scene = QGraphicsScene(self)


        self.widget = QWidget()
        self.widget.setLayout(self._layout)
        self.setCentralWidget(self.widget)
        self.rects = []
        # self._begin

        # self.layout.addWidget(SelectAreaWidget)

    def loadFile(self):
        self.fileName = QFileDialog.getOpenFileName(self)
        self.loadImage()

    def loadImage(self):
        fPath = self.fileName[0]
        if fPath != "":
            # for i in reversed(range(self.layout.count())):
            #     self.layout.itemAt(i).widget().setParent(None)
            # self.layout.
            self.v = SelectAreaGraphicScene.View(fPath, self.scene)
            self.setCentralWidget(self.v)
            # self.label.setPixmap(QPixmap(fPath))
            # self.label.setFixedSize(self.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())
