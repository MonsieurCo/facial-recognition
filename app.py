import sys, random
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGraphicsView, QMainWindow, QApplication, QLabel, QVBoxLayout
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget

from widgets.multiview import MultiView
from widgets import SelectAreaWidget, MenuBar


class ImageAnnotator(QtWidgets.QWidget):

    def __init__(self):
        super(ImageAnnotator, self).__init__()
        self.title = "ImageAnnotator"
        self.setWindowTitle(self.title)
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

        self.fileName = None
        self.begin, self.destination = QPoint(), QPoint()

        self.layout.addWidget(SelectAreaWidget(self))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())