import sys

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, \
    QWidget

from widgets import SelectAreaWidget


class ImageAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "ImageAnnotator"
        self.setWindowTitle(self.title)
        # self.setFixedSize(QSize(1280, 720))
        self.resize(1280, 720)
        # self.loadImage()

        self.button = QtWidgets.QPushButton("Load files")
        self.button.clicked.connect(self.loadFile)

        self.label = QLabel(self)
        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.fileName = None
        self.begin, self.destination = QPoint(), QPoint()

        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignBottom)
        self.layout.addWidget(SelectAreaWidget(self))

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
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
            self.pixmap = QPixmap(fPath)
            self.label.setPixmap(self.pixmap)
            self.label.setFixedSize(self.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())
