
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QGridLayout, QLabel, QVBoxLayout
from typing import Optional

from widgets.ImageButton import ImageButton


class MultiView(QtWidgets.QScrollArea):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.size = parent.size()
        self.button = QtWidgets.QPushButton("Load folder")
        self.button.clicked.connect(self.loadFiles)
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.gridButtons : QGridLayout = QtWidgets.QGridLayout(self)
        self.gridButtons.setColumnMinimumWidth(4,4)
        self.label = QLabel(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.gridButtons)
        self.layout.addWidget(self.button)



    @QtCore.Slot()
    def loadFiles(self):
        for i in reversed(range(self.gridButtons.count())):
            self.gridButtons.itemAt(i).widget().setParent(None)

        dir_path = QFileDialog.getExistingDirectory(self)
        dir = QDir(dir_path)
        filter = ["*.png", "*.xpm", "*.jpg"]
        dir.setNameFilters(filter)

        for i in range(min(len(dir.entryList()),30)):
            name = dir.entryList()[i]
            path = QDir.filePath(dir,name)
            self.gridButtons.addWidget(ImageButton(name,path,i,self))

