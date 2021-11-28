from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QGridLayout, QLabel, QVBoxLayout, QWidget
from typing import Optional

from src.ImageButtonWidget import ImageButton
from src.FrameImageWidget import FrameImage


class MultiView(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)

        self.size = parent.size()
        self.pageSize = 60
        self.dirSize = 0
        self.dir = None
        self.previousPageWidgets = []
        self.NextPageWidgets = []
        self.pages = []
        self.nbPages = 0
        self.currentPage = 0

        self.setAcceptDrops(True)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)

        self.label = QLabel(self)
        self.setLayout(self.layout)

        self.gridButtons: QGridLayout = QtWidgets.QGridLayout(self)
        self.gridButtons.setColumnMinimumWidth(4, 1)
        self.gridButtons.setRowMinimumHeight(6, 1)

        self.grid = QtWidgets.QWidget(self)
        self.grid.setLayout(self.gridButtons)


        self.bottomLayout: QGridLayout = QtWidgets.QGridLayout(self)
        self.bottomLayout.setColumnMinimumWidth(2, 2)

        self.changeWidget = QWidget(self)
        self.changeWidget.setLayout(self.bottomLayout)

        self.ButtonPrevious = QtWidgets.QPushButton(icon = QIcon("ressources/left.png"))
        self.ButtonNext = QtWidgets.QPushButton(icon = QIcon("ressources/right.png"))

        self.ButtonNext.clicked.connect(self.chargeNextPage)
        self.ButtonPrevious.clicked.connect(self.chargePreviousPage)

        self.ButtonPrevious.setVisible(False)
        self.ButtonNext.setVisible(False)

        self.bottomLayout.addWidget(self.ButtonPrevious)
        self.bottomLayout.addWidget(self.ButtonNext)

        self.layout.addWidget(self.grid,alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.changeWidget,alignment=QtCore.Qt.AlignBottom)


    def load(self):

        dirPath = QFileDialog.getExistingDirectory(self)
        self.loadFolder(dirPath)

    def loadFolder(self, dirPath):
        for i in reversed(range(self.gridButtons.count())):
            self.gridButtons.itemAt(i).widget().setParent(None)

        self.dir = QDir(dirPath)
        filtered = ["*.png", "*.xpm", "*.jpg"]
        self.dir.setNameFilters(filtered)
        self.dirSize = len(self.dir.entryList())

        self.nbPages = self.dirSize // self.pageSize

        if self.dirSize == 0 :
            return

        for i in range(self.nbPages + 2):
            self.pages.append(min(len(self.dir.entryList()), self.pageSize * i))

        self.display(self.currentPage)
        if self.dirSize > self.pageSize:
            self.ButtonNext.setVisible(True)
            self.ButtonPrevious.setVisible(True)
        else :
            self.ButtonNext.setVisible(False)
            self.ButtonPrevious.setVisible(False)

    def chargeNextPage(self):
        if self.currentPage + 1 <= self.nbPages:
            self.currentPage += 1
            self.display(self.currentPage)

        else:
            self.currentPage = 0
            self.display(self.currentPage)

    def chargePreviousPage(self):

        if self.currentPage - 1 >= 0:
            self.currentPage -= 1
            self.display(self.currentPage)

        else:
            self.currentPage = self.nbPages
            self.display(self.currentPage)

    def display(self, pageNb):
        for i in reversed(range(self.gridButtons.count())):
            wid = self.gridButtons.itemAt(i).widget()
            self.gridButtons.removeWidget(wid)
            wid.setParent(None)

        self.gridButtons.update()
        for i in range(self.pages[pageNb], self.pages[pageNb + 1]):
            name = self.dir.entryList()[i]
            path = QDir.filePath(self.dir, name)
            self.gridButtons.addWidget(ImageButton(name, path, i, self),i//6,i%6, QtCore.Qt.AlignTop)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        url = e.mimeData().urls()[0]
        path = url.toLocalFile()
        if path[-4:] == ".png" or path[-4:] == ".xpm" or path[-4:] == ".jpg":
            FrameImage(path, path, None).show()
        else:
            self.loadFolder(path)