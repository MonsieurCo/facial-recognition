import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel, QVBoxLayout, \
    QWidget
from qt_material import apply_stylesheet

from widgets import MenuBar
from widgets.multiview import MultiView

# from qt_material import apply_stylesheet
import qdarkstyle

class ImageAnnotator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageAnnotator")
        self.resize(1280, 720)

        self.button = QtWidgets.QPushButton("Load files")
        self.label = QLabel(self)
        self.fold = MultiView(self.label)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.fold)
        self.layout.addWidget(self.button)
        self.setMenuBar(MenuBar())

        self.dialog = QFileDialog(self, "Open Image", filter="Images (*.png *.xpm *.jpg)")
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())
