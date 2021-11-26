from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QGridLayout, QLabel, QVBoxLayout, QWidget
from typing import Optional

from widgets.ImageButton import ImageButton


class MultiView(QtWidgets.QScrollArea):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.size = parent.size()
        self.pagesize = 10
        self.dir_size = 0
        self.otherImages = []
        self.dir = None
        self.previousPageWidgets = []
        self.NextPageWidgets = []


        self.button = QtWidgets.QPushButton("Load folder")
        self.button.clicked.connect(self.loadFiles)
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.gridButtons: QGridLayout = QtWidgets.QGridLayout(self)
        self.gridButtons.setColumnMinimumWidth(4, 4)
        self.label = QLabel(self)
        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.gridButtons)

        self.bottomLayout: QGridLayout = QtWidgets.QGridLayout(self)
        self.bottomLayout.setColumnMinimumWidth(8, 8)

        self.changeWidget = QWidget(self)
        self.changeWidget.setLayout(self.bottomLayout)


        self.ButtonPrevious = QtWidgets.QPushButton("<--")
        self.ButtonNext = QtWidgets.QPushButton("-->")
        self.ButtonNext.clicked.connect(self.chargeNextPage)
        self.ButtonPrevious.clicked.connect(self.chargePreviousPage)

        self.ButtonPrevious.setVisible(False)
        self.ButtonNext.setVisible(False)


        self.bottomLayout.addWidget(self.ButtonPrevious)
        self.bottomLayout.addWidget(self.ButtonNext)

        self.layout.addWidget(self.changeWidget)
        self.layout.addWidget(self.button)


    @QtCore.Slot()
    def loadFiles(self):
        for i in reversed(range(self.gridButtons.count())):
            self.gridButtons.itemAt(i).widget().setParent(None)

        dir_path = QFileDialog.getExistingDirectory(self)
        self.dir = QDir(dir_path)
        filter = ["*.png", "*.xpm", "*.jpg"]
        self.dir.setNameFilters(filter)
        self.dir_size = len(self.dir.entryList())
        for i in range(min(self.dir_size, self.pagesize)):
            name = self.dir.entryList()[i]
            path = QDir.filePath(self.dir, name)
            self.gridButtons.addWidget(ImageButton(name, path, i, self))
        if self.dir_size > self.pagesize:
            self.otherImages = self.dir.entryList()[min(self.dir_size, self.pagesize):]
            self.ButtonPrevious.setVisible(True)
            self.ButtonNext.setVisible(True)


    @QtCore.Slot()
    def chargeNextPage(self):
        for i in reversed(range(self.gridButtons.count())):
            self.previousPageWidgets.append(self.gridButtons.itemAt(i).widget())
            self.gridButtons.itemAt(i).widget().setVisible(False)

        if len(self.NextPageWidgets) > 1 :
            for w in self.NextPageWidgets:
                w.setVisible(True)
        else:
            for i in range(min(len(self.otherImages), self.pagesize)):
                name = self.otherImages[i]
                path = QDir.filePath(self.dir, name)
                self.gridButtons.addWidget(ImageButton(name, path, i, self))
        self.NextPageWidgets = []
        if len(self.otherImages) > self.pagesize:
            self.otherImages =  self.dir.entryList()[min(len(self.otherImages), self.pagesize):]
            self.ButtonPrevious.setVisible(True)
            self.ButtonNext.setVisible(True)

    @QtCore.Slot()
    def chargePreviousPage(self):
        for i in reversed(range(self.gridButtons.count())):
            self.NextPageWidgets.append(self.gridButtons.itemAt(i).widget())
            self.gridButtons.itemAt(i).widget().setVisible(False)

        for w in self.previousPageWidgets:
            w.setVisible(True)
        self.previousPageWidgets = []
