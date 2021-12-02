from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog


class CategoryBar(QtWidgets.QMenuBar):

    def __init__(self, parent: Optional[QtWidgets.QMainWindow] = ...) -> None:
        super().__init__()

        self.parent = parent
        self.impor = QtWidgets.QMenu("Import")
        self.open = QAction("Import from...")

        self.open.triggered.connect(self.load)
        self.impor.addAction(self.open)
        self.addMenu(self.impor)

    def load(self):
        filename = QFileDialog(self)
        fpath = filename.getOpenFileName(self)[0]
        ext = fpath.split(".")[1]
        print(ext)
        if ext == "csv":
            self.parent.loadCategoriesFileCSV(fpath)

        elif ext == "json":
            self.parent.loadCategoriesFileJSON(fpath)

