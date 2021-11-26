import sys, random
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGraphicsView, QMainWindow, QApplication, QLabel, QVBoxLayout
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget
import sys

import PySide6.QtGui
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QPoint, QSize, QRect
from PySide6.QtGui import QPixmap, QPainter, QMouseEvent
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, \
    QWidget, QGraphicsScene

from widgets.multiview import MultiView
from widgets import SelectAreaWidget, MenuBar

from widgets import SelectAreaGraphicScene

class ImageAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageAnnotator")
        # self.setFixedSize(QSize(1280, 720))
        self.resize(1280, 720)

        self.button = QtWidgets.QPushButton("Load files")
        self.label = QLabel(self)
        self.fold = MultiView(self.label)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.fold)
        self.layout.addWidget(self.button)

        self.menue = MenuBar(None)
        self.layout.addWidget(self.menue)

        self.dialog = QFileDialog(self, "Open Image", filter="Images (*.png *.xpm *.jpg)")
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self._layout: QVBoxLayout = QVBoxLayout(self)

        self.fileName = None
        self.begin, self.destination = QPoint(), QPoint()


        self._layout.addWidget(self.button)

        self.scene = QGraphicsScene(self)

        self.layout.addWidget(SelectAreaWidget(self))

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