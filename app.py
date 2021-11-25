import sys, random
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGraphicsView, QMainWindow, QApplication, QLabel, QVBoxLayout

from widgets.multiview import MultiView


class ImageAnnotator(QtWidgets.QWidget):

    def __init__(self):
        super(ImageAnnotator, self).__init__()
        self.title = "ImageAnnotator"
        self.setWindowTitle(self.title)
        #self.setFixedSize(QSize(1280, 720))
        self.resize(1280, 720)
        # self.loadImage()


        self.button = QtWidgets.QPushButton("Load files")
        self.label = QLabel(self)
        self.fold = MultiView(self)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.fold)
        self.layout.addWidget(self.button)

        self.dialog = QFileDialog(self, "Open Image", filter="Images (*.png *.xpm *.jpg)")
        self.dialog.setFileMode(QFileDialog.AnyFile)

        self.button.clicked.connect(self.loadFile)
        self.fileName = None


    @QtCore.Slot()
    def loadFile(self):
        self.fileName = QFileDialog.getOpenFileName(self)
        self.loadImage()

    def loadImage(self):
        fPath = self.fileName[0]
        if fPath != "":
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
            pixmap = QPixmap(fPath)

            self.label.setPixmap(pixmap)
            self.label.setFixedSize(self.size())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())