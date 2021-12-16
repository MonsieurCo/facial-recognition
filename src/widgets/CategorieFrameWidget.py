import json
from typing import Optional

import PySide6.QtWidgets
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import SIGNAL, QPoint
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import QLineEdit, QFormLayout, QPushButton, QHBoxLayout, QListView

import src.widgets.CategoryMenuBar as CategoryMenuBar
from src.QtColors import QtColors
from src.annotations import AnnotateManager, Annotation
from src.widgets import rects


class CategorieFrame(QtWidgets.QMainWindow):
    def __init__(self, fPath, begin: QPoint, destination: QPoint, currentRect: QtWidgets.QGraphicsRectItem, imgSize,
                 parent: Optional[QtWidgets.QWidget] = ..., isEditing=False) -> None:
        super().__init__()
        self.begin = begin
        self.destination = destination
        self.currentRect = currentRect
        self.parent = parent
        self.isEditing = isEditing
        self.listView = QListView(self)
        self.categories = ["Masque",
                           "Pas de masque"]
        self.fpathCSV = ""
        self.fpathJSON = ""
        self.isJSON = False
        self.lineEdit = QLineEdit()
        self.addCat = QPushButton()
        self.addCat.setText("Ok")
        self.imgSize = imgSize

        self.connect(self.addCat, SIGNAL("clicked()"), self.addCategory)

        self.model = QStandardItemModel(self.listView)

        self.loadCategories()

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
        self.setWindowTitle(self.currentRect.choice)

    def validate(self):
        choice = self.categories[self.itemSelectedIndex]
        if self.isEditing:
            annotations = AnnotateManager.annotations[self.fName]["annotations"]
            for annotation in annotations:
                if annotation["id"] == id(self.currentRect):
                    annotation["categorie"] = choice
                    annotation["categorie_id"] = self.itemSelectedIndex
                    break
            self.currentRect.setBrush(QtColors.COLORS[self.itemSelectedIndex % QtColors.lengthColors])
            self.currentRect.choice = choice
            # sm = self.listView.selectionModel()
            # sm.select(self.model.itemFromIndex(self.itemSelectedIndex), QtCore.QItemSelectionModel.Select)
            # sm.select(self.itemSelectedIndex, QtCore.QItemSelectionModel.Select)

        else:
            AnnotateManager.addAnnotation(self.fName,
                                          Annotation(
                                              id(self.currentRect),
                                              self.begin,
                                              self.destination,
                                              choice,
                                              self.fPath,
                                              self.itemSelectedIndex,
                                              self.imgSize[0],
                                              self.imgSize[1]
                                          ))
            self.currentRect.setBrush(QtColors.COLORS[self.itemSelectedIndex % QtColors.lengthColors])
            self.currentRect.choice = choice
            # self.list
            try:
                rects.RECTS[self.fName].append(self.currentRect)
            except:
                rects.RECTS[self.fName] = [self.currentRect]

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

        if self.fpathCSV != "" and not self.isJSON:
            newCategorie = self.lineEdit.text()
            self.categories.append(newCategorie)
            # string = ",".join(self.categories)
            with open(self.fpathCSV, "a") as f:
                f.write("," + newCategorie)
        else:
            if self.fpathJSON == "":
                self.fpathJSON = "./ressources/categories.json"
                self.isJSON = True
            newCategorie = self.lineEdit.text()
            self.categories.append(newCategorie)
            data = []
            for c in self.categories:
                temp = {"category": c}
                data.append(temp)
            json_object = json.dumps(data, indent=2)

            with open(self.fpathJSON, "w") as outfile:
                outfile.write(json_object)

        self.loadCategories()

    def deleteCategory(self):
        if self.listView.selectedIndexes() != []:
            selectedCategorie = self.listView.currentIndex().data()
            self.categories.remove(selectedCategorie)
        if self.fpathCSV != "" and not self.isJSON:

            string = ",".join(self.categories)
            with open(self.fpathCSV, "w+") as f:
                f.write(string)

        elif self.isJSON:
            self.categories.remove(selectedCategorie)
            data = []
            for c in self.categories:
                temp = {"category": c}
                data.append(temp)
            json_object = json.dumps(data, indent=2)

            with open(self.fpathJSON, "w") as outfile:
                outfile.write(json_object)

        self.loadCategories()

    def loadCategories(self):
        self.model.clear()
        for category in self.categories:
            item = QStandardItem(category)
            item.setEditable(False)
            self.model.appendRow(item)

    def loadCategoriesFileCSV(self, fpathCSV):
        if fpathCSV != "":
            self.fpathCSV = fpathCSV
            self.isJSON = False
            self.fpathJSON = ""
            fd = open(fpathCSV)
            lines = " ".join(fd.readlines())
            cat = lines.split(",")

            self.categories = cat
            self.loadCategories()

    def loadCategoriesFileJSON(self, fpathJSON):

        if fpathJSON != "":
            self.fpathJSON = fpathJSON
            self.fpathCSV = ""
            self.isJSON = True
            fd = open(fpathJSON)
            data = json.load(fd)
            categories = []
            for d in data:
                categories.append(d["category"])
            self.categories = categories
            self.loadCategories()

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        try:
            if not self.currentRect in rects.RECTS[self.fName]:
                self.parent.getScene().removeItem(self.currentRect)
        except:
            pass
