from typing import Optional

import PySide6.QtWidgets
from PySide6.QtCore import SIGNAL
from PySide6.QtWidgets import QLineEdit, QFormLayout, QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QListView
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QAction, QIcon
from PySide6.QtWidgets import QFileDialog

from src import widgets
from src.widgets.CategoryMenuBar import CategoryBar


class CategorieFrame(QtWidgets.QMainWindow):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent)
        self.parent = parent
        self.listView = QListView(self)
        self.categories = ["Masque",
                           "Pas de masque"]

        self.lineEdit = QLineEdit()

        self.addCat = QPushButton()
        self.addCat.setText("Ok")

        self.connect(self.addCat, SIGNAL("clicked()"), self.addCategory)

        self.model = QStandardItemModel(self.listView)

        self.loadCategories()

        self.listView.clicked[QtCore.QModelIndex].connect(self.onItemSelected)
        self.listView.setModel(self.model)
        self.itemSelectedIndex = None
        self.oldItem = QStandardItem()
        self.button = QtWidgets.QPushButton(icon = QIcon("ressources/32x32validate.png"),text = "\tSelect category")
        self.button.setEnabled(False)
        self.button.clicked.connect(self.validate)

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
        self._close()

    def _close(self):
        self.close()

    def onItemSelected(self, index):
        item = self.model.itemFromIndex(index)
        self.itemSelectedIndex = item.row()
        item.setForeground(QBrush(QColor(255, 0, 0)))
        self.oldItem.setForeground(QColor(255, 255, 255))
        self.oldItem = item
        self.button.setEnabled(True)

    def addCategory(self):
        newCategorie = self.lineEdit.text()
        self.categories.append(newCategorie)
        self.loadCategories()

    def deleteCategory(self):
        if self.listView.selectedIndexes() != []:
            selectedCategorie = self.listView.currentIndex().data()
            self.categories.remove(selectedCategorie)
            self.loadCategories()

    def loadCategories(self):
        self.model.clear()
        for category in self.categories:
            item = QStandardItem(category)
            item.setEditable(False)
            self.model.appendRow(item)


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
