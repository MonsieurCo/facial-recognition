from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon, QPainter
from PySide6.QtWidgets import QVBoxLayout
from typing import Optional


class ImageButton(QtWidgets.QWidget):
    def __init__(self,name,path,i, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.layout : QVBoxLayout = QVBoxLayout(self)
        self.path = path
        self.button = QtWidgets.QPushButton(f"Image n°{i} : {name}")
        self.icon = QtGui.QIcon(path)
        self.button.setFixedSize(90, 90)
        self.button.setStyleSheet(f"border-image : url({self.path}) 0 0 0 0 stretch stretch ; border-radius: 15px; border-width: 2px;")
        self.button.setIcon(self.icon)
        self.button.clicked.connect(self.openFile())
        self.setFixedSize(100, 100)
        self.layout.addWidget(self.button)

    def openFile(self):
        pixmap = QPixmap(self.path)
        #ouvrir une nouvelle fenetre ici
        # self.label.setPixmap(pixmap)
        # self.label.setFixedSize(self.size())

    def drawIcon(self, painter, pos):
        enabledStatus = QIcon.Active
        pixmap = self.icon.pixmap(self.button.size(), enabledStatus, QIcon.On)
        painter.drawPixmap(pos, pixmap)