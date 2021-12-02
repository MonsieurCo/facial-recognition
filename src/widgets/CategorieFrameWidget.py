from typing import Optional

import PySide6.QtWidgets
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import SIGNAL, QPoint
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import QLineEdit, QFormLayout, QPushButton, QHBoxLayout, QListView

import src.widgets.CategoryMenuBar as CategoryMenuBar
from src import RECTS
from src.annotations import AnnotateManager, Annotation


class CategorieFrame(QtWidgets.QMainWindow):
    def __init__(self, fPath, begin: QPoint, destination: QPoint, currentRect: QtWidgets.QGraphicsRectItem,
                 parent: Optional[QtWidgets.QWidget] = ..., isEditing=False) -> None:
        super().__init__()
        self.begin = begin
        self.destination = destination
        self.currentRect = currentRect
        self.parent = parent
        self.isEditing = isEditing
        self.listView = QListView(self)
        # self.categories = ["Masque",
        #                   "Pas de masque"]
        self.fpathCSV = "./ressources/categories.csv"

        self.lineEdit = QLineEdit()

        self.addCat = QPushButton()
        self.addCat.setText("Ok")

        self.connect(self.addCat, SIGNAL("clicked()"), self.addCategory)

        self.model = QStandardItemModel(self.listView)

        self.loadCategoriesFile(self.fpathCSV)

        self.listView.clicked[QtCore.QModelIndex].connect(self.onItemSelected)
        self.listView.setModel(self.model)
        self.itemSelectedIndex = None
        self.oldItem = QStandardItem()

        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]

        self.buttonSelectCategory = QtWidgets.QPushButton(icon=QIcon("ressources/32x32validate.png"),
                                                          text="\tSelect category")
        self.buttonSelectCategory.setEnabled(False)
        self.buttonSelectCategory.clicked.connect(self.validate)

        self.buttonDeleteCategory = QtWidgets.QPushButton(icon=QIcon("ressources/32x32delete.png"),
                                                          text="\tDelete category")
        self.buttonDeleteCategory.setEnabled(False)
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

        self.menu = CategoryMenuBar.CategoryBar(self)
        self.setMenuBar(self.menu)

    def validate(self):
        choice = self.categories[self.itemSelectedIndex]
        if self.isEditing:
            annotations = AnnotateManager.annotations[self.fName]["annotations"]
            for annotation in annotations:
                if annotation["id"] == id(self.currentRect):
                    annotation["categorie"] = choice
        else:
            AnnotateManager.addAnnotation(self.fName,
                                          Annotation(
                                              id(self.currentRect),
                                              self.begin,
                                              self.destination,
                                              choice,
                                              self.fPath
                                          ))
            try:
                RECTS[self.fName].append(self.currentRect)
            except:
                RECTS[self.fName] = [self.currentRect]
            self.parent.getScene().addItem(self.currentRect)
        self._close()

    def _close(self):
        self.close()

    def onItemSelected(self, index):
        item = self.model.itemFromIndex(index)
        self.itemSelectedIndex = item.row()
        self.buttonSelectCategory.setEnabled(True)
        self.buttonDeleteCategory.setEnabled(True)

    def addCategory(self):
        if self.fpathCSV != "":
            newCategorie = self.lineEdit.text()
            self.categories.append(newCategorie)
            # string = ",".join(self.categories)
            with open(self.fpathCSV, "a") as f:
                f.write("," + newCategorie)

            self.loadCategories()

    def deleteCategory(self):
        if self.fpathCSV != "":
            if self.listView.selectedIndexes() != []:
                selectedCategorie = self.listView.currentIndex().data()
                self.categories.remove(selectedCategorie)
                string = ",".join(self.categories)
                with open(self.fpathCSV, "w+") as f:
                    f.write(string)

                self.loadCategoriesFile(self.fpathCSV)

    def loadCategories(self):
        self.model.clear()
        for category in self.categories:
            item = QStandardItem(category)
            item.setEditable(False)
            self.model.appendRow(item)

    def loadCategoriesFile(self, fpathCSV):
        # ./ressources/categories.csv
        self.fpathCSV = fpathCSV
        if fpathCSV != "":
            fd = open(fpathCSV)
            lines = " ".join(fd.readlines())
            cat = lines.split(",")

            self.categories = cat
            self.model.clear()
            for categorie in self.categories:
                item = QStandardItem(categorie)
                item.setEditable(False)
                self.model.appendRow(item)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        try:
            if not self.currentRect in RECTS[self.fName]:
                self.parent.getScene().removeItem(self.currentRect)
        except:
            pass
