from typing import Optional

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QAction, QIcon
from PySide6.QtWidgets import QFileDialog

from src import AnnotateManager, Annotation

from src import widgets
from src.widgets.CategoryMenuBar import CategoryBar


class CategorieFrame(QtWidgets.QMainWindow):
    def __init__(self, fPath, coords, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent)
        self.coords = coords
        self.parent = parent
        self.listView = QtWidgets.QListView(self)
        self.categories = ["Masque"
                           "test2",
                           "test3"]

        self.model = QStandardItemModel(self.listView)
        for categorie in self.categories:
            item = QStandardItem(categorie)
            item.setEditable(False)
            self.model.appendRow(item)

        self.listView.clicked[QtCore.QModelIndex].connect(self.onItemSelected)
        self.listView.setModel(self.model)
        self.itemSelectedIndex = None
        self.oldItem = QStandardItem()
        self.button = QtWidgets.QPushButton(icon = QIcon("ressources/32x32validate.png"),text = "\tSelect category")
        self.button.setEnabled(False)
        self.button.clicked.connect(self.validate)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.listView)
        self.layout.addWidget(self.button)
        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        self.central = QtWidgets.QWidget()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

        self.menu = CategoryBar(self)
        self.setMenuBar(self.menu)


    def validate(self):
        AnnotateManager.addAnnotation(self.fName,
                                           Annotation(
                                               self.coords[0],
                                               self.coords[1],
                                               self.categories[self.itemSelectedIndex],
                                               self.fPath
                                           ))
        self._close()

    def _close(self):
        self.close()

    def onItemSelected(self, index):
        item = self.model.itemFromIndex(index)
        self.itemSelectedIndex = item.row()

    def loadCategories(self,fpath):
        #./ressources/categories.csv

        if fpath != "":
            fd = open(fpath)
            lines = " ".join(fd.readlines())
            cat = lines.split(",")

            self.categories = cat
            self.model.clear()
            for categorie in self.categories:
                item = QStandardItem(categorie)
                item.setEditable(False)
                self.model.appendRow(item)