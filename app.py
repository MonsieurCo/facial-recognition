import sys

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget

from widgets import SelectAreaWidget, MenuBar


class ImageAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "ImageAnnotator"
        self.setWindowTitle(self.title)
        # self.setFixedSize(QSize(1280, 720))
        self.resize(1280, 720)
        # self.loadImage()

        self.label = QLabel(self)
        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.menue = MenuBar(self.label)
        self.layout.addWidget(self.menue)

        self.fileName = None
        self.begin, self.destination = QPoint(), QPoint()

        self.layout.addWidget(SelectAreaWidget(self))

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        # self.layout.addWidget(SelectAreaWidget)

    @QtCore.Slot()
    def magic(self):
        self.loadImage()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())
