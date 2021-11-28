from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout
from typing import Optional

from src.widgets.FrameImageWidget import FrameImage


class ImageButton(QtWidgets.QWidget):
    def __init__(self, name, path, i, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.path = path
        self.name = name
        self.button = QtWidgets.QPushButton(f"Image n°{i} ")  #:\n {name}
        self.icon = QIcon(path)
        self.button.setIcon(self.icon)
        self.button.clicked.connect(self.openFrame)
        self.setFixedSize(200, 50)
        self.layout.addWidget(self.button)

    def openFrame(self):
        self.frame = FrameImage(self.path, self.name, None)
        self.frame.show()
