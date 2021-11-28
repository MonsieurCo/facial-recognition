import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, \
    QWidget

from src import MenuBar, MultiView


class ImageAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageAnnotator")
        self.resize(1280, 720)

        self.label = QLabel(self)
        self.frame = MultiView(self)

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
    with open("styles/dark-theme.qss") as f:
        lines = " ".join(f.readlines())
    app.setStyleSheet(lines)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())
