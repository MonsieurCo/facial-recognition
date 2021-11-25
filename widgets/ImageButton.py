from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout
from typing import Optional


class ImageButton(QtWidgets.QWidget):
    def __init__(self,name,path,i, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.layout : QVBoxLayout = QVBoxLayout(self)
        self.path = path
        self.button = QtWidgets.QPushButton(f" Image {i} :\n {name}")
        self.button.setStyleSheet(f"border-image : url({self.path}) 0 0 0 0 stretch stretch ;border-width: 2px;border-radius: 10px;")
        #*self.button.styleSheet().
        self.button.clicked.connect(self.openFile())
        self.button.setFixedSize(90, 90)
        self.setFixedSize(100, 100)
        self.layout.addWidget(self.button)


    def openFile(self):
        pixmap = QPixmap(self.path)
        #ouvrir une nouvelle fenetre ici
        # self.label.setPixmap(pixmap)
        # self.label.setFixedSize(self.size())
