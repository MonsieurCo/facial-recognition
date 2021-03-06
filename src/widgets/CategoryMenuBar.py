from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog


class CategoryBar(QtWidgets.QMenuBar):

    def __init__(self, parent: Optional[QtWidgets.QMainWindow] = ...) -> None:
        super().__init__()
        """
        this class is a custom class of a menu bar for the category selection frame
        :returns a Category Menu Bar
        :rtype: CategoryBar

        """
        self.parent = parent
        self.impor = QtWidgets.QMenu("Import")
        self.open = QAction("Import categories")
        self.open.triggered.connect(self.load)

        self.close = QAction("Close", self)
        self.close.setShortcut("Ctrl+w")
        self.close.triggered.connect(self.closeImage)

        self.impor.addAction(self.open)
        self.impor.addAction(self.close)
        self.addMenu(self.impor)

    def load(self):
        """
        Open a Dialog box to choose a category file to load categories
        and transmit the path to the cCategoryFrameWidget
        :return:
        """
        filename = QFileDialog(self)
        fpath = filename.getOpenFileName(self)[0]
        ext = fpath.split(".")[1]
        if ext == "csv":
            self.parent.loadCategoriesFileCSV(fpath)

        elif ext == "json":
            self.parent.loadCategoriesFileJSON(fpath)

    def closeImage(self):
        """
        Close the parent frame that contains the image
        """
        if self.parent is not None:
            self.parent.close()
