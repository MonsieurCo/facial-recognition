import ctypes
import sys

from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QMainWindow, QApplication, QVBoxLayout, \
    QWidget, QLineEdit

from src.widgets.MenuBarWidget import MenuBar
from src.widgets.MultiViewWidget import MultiView


class ImageAnnotator(QMainWindow):

    def __init__(self):
        """
        Main class that run the application
        """
        super().__init__()
        self.setWindowTitle("ImageAnnotator")
        self.resize(1280, 720)
        edit = QLineEdit()
        edit.setDragEnabled(True)

        self.frame = MultiView(self)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.layout.addWidget(self.frame)
        self.setMenuBar(MenuBar(True, self))

        self.dialog = QFileDialog(self, "Open Image", filter="Images (*.png *.xpm *.jpg)")
        self.dialog.setFileMode(QFileDialog.AnyFile)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        sys.exit(0)


if __name__ == "__main__":
    """
    run the program
    """
    if sys.platform == "win32":
        appId = 'ImageAnnotator'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)
    app = QApplication(sys.argv)
    with open("ressources/styles/dark-theme.qss") as f:
        lines = " ".join(f.readlines())
    app.setStyleSheet(lines)
    app.setWindowIcon(QIcon("ressources/assets/app-logo.png"))
    app.setDesktopFileName("ImageAnnotator")

    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())
