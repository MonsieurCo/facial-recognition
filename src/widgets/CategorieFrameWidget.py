from typing import Optional, overload

import PySide6.QtWidgets
from PySide6.QtCore import SIGNAL
from PySide6.QtWidgets import QLineEdit, QFormLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QListView
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
        self.listView = QListView(self)
        # self.categories = ["Masque",
        #                   "Pas de masque"]
        self.fpath = "./ressources/categories.csv"

        self.lineEdit = QLineEdit()

        self.addCat = QPushButton()
        self.addCat.setText("Ok")

        self.connect(self.addCat, SIGNAL("clicked()"), self.addCategory)

        self.model = QStandardItemModel(self.listView)

        self.loadCategoriesFile(self.fpath)

        self.listView.clicked[QtCore.QModelIndex].connect(self.onItemSelected)
        self.listView.setModel(self.model)
        self.itemSelectedIndex = None
        self.oldItem = QStandardItem()
        self.button = QtWidgets.QPushButton(icon=QIcon("ressources/32x32validate.png"), text="\tSelect category")
        self.button.setEnabled(False)
        self.button.clicked.connect(self.validate)

        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]


        self.buttonSelectCategory = QtWidgets.QPushButton("Select category", self)
        self.buttonSelectCategory.clicked.connect(self.validate)

        self.buttonDeleteCategory = QtWidgets.QPushButton("Delete category", self)
        self.buttonDeleteCategory.clicked.connect(self.deleteCategory)

        self.addCategoryWidget = QHBoxLayout()
        self.addCategoryWidget.addWidget(self.lineEdit)
        self.addCategoryWidget.addWidget(self.addCat)
        self.addCategoryWidget.addStretch()

        self.layout = QFormLayout()

        self.layout.addRow("Add category", self.addCategoryWidget)
        self.layout.addRow(self.listView)
        self.layout.addRow(self.buttonSelectCategory)
        self.layout.addRow(self.buttonDeleteCategory)
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
        self.button.setEnabled(True)

    def addCategory(self):
        if self.fpath != "":
            newCategorie = self.lineEdit.text()
            self.categories.append(newCategorie)
            #string = ",".join(self.categories)
            with open (self.fpath, "a") as f:
                f.write(","+newCategorie)

            self.loadCategories()

    def deleteCategory(self):
        if self.fpath != "":
            if self.listView.selectedIndexes() != []:
                selectedCategorie = self.listView.currentIndex().data()
                self.categories.remove(selectedCategorie)
                string = ",".join(self.categories)
                with open(self.fpath, "w+") as f:
                    f.write(string)

                self.loadCategoriesFile(self.fpath)

    def loadCategories(self):
        self.model.clear()
        for category in self.categories:
            item = QStandardItem(category)
            item.setEditable(False)
            self.model.appendRow(item)

    def loadCategoriesFile(self, fpath):
        # ./ressources/categories.csv
        self.fpath = fpath
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