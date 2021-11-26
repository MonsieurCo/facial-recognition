from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QDir
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGridLayout, QLabel, QVBoxLayout
from typing import Optional

from widgets import FrameImage, MenuBar


class ImageButton(QtWidgets.QWidget):
    def __init__(self, name, path, i, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.path = path
        self.button = QtWidgets.QPushButton(f"Image n°{i} ") #:\n {name}
        self.icon = QtGui.QIcon(path)
        # self.button.setFixedSize(90, 90)
        #self.button.setStyleSheet(f"border-image : url({self.path}) 0 0 0 0 stretch stretch ; border-radius: 15px; border-width: 2px;")
        self.button.setIcon(self.icon)
        self.button.clicked.connect(self.openFile())
        self.setFixedSize(200, 50)
        self.layout.addWidget(self.button)

    def openFrame(self):
        self.frame=FrameImage(self.path, self.name,  None)
        self.frame.menue = MenuBar(self.frame)
        #self.frame.layout.addWidget(self.frame.menue) #TODO a fix ça reecrit sur le layout donc empehce les carrés
        self.frame.show()




