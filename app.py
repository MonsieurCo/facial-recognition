import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, \
    QWidget

from widgets import MenuBar
from widgets.multiview import MultiView


class ImageAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageAnnotator")
        self.resize(1280, 720)

        self.label = QLabel(self)
        self.frame = MultiView(self.label)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.frame)
        self.setMenuBar(MenuBar(True, self))

        self.dialog = QFileDialog(self, "Open Image", filter="Images (*.png *.xpm *.jpg)")
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())
