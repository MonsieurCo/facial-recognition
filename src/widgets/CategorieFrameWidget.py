import json
from typing import Optional

import PySide6.QtWidgets
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import SIGNAL, QPoint
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtWidgets import QLineEdit, QFormLayout, QPushButton, QHBoxLayout, QListView, QFileDialog
import json
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


        self.lineEdit = QLineEdit()
        self.addCat = QPushButton()
        self.addCat.setText("Ok")
        self.imgSize = imgSize

        self.connect(self.addCat, SIGNAL("clicked()"), self.addCategory)

        self.model = QStandardItemModel(self.listView)

        self.loadCategoriesFileCSV(self.parent.fpathCSV)

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

        self.buttonChangeCategory = QtWidgets.QPushButton(  # icon=QIcon("ressources/32x32delete.png"),
            text="\tChange category")
        self.buttonChangeCategory.setEnabled(False)
        self.buttonChangeCategory.clicked.connect(self.changeCategory)

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
        self.layout.addRow(self.buttonChangeCategory)
        self.layout.addRow(self.buttonDeleteCategory)
        self.central = QtWidgets.QWidget()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

        self.menu = CategoryMenuBar.CategoryBar(self)
        self.setMenuBar(self.menu)
        self.setWindowTitle(self.currentRect.choice)


        if self.parent.isJSON and self.parent.fpathJSON != "" :
            self.loadCategoriesFileJSON(self.parent.fpathJSON)
        elif not self.parent.isJSON and self.parent.fpathCSV != "" :
            self.loadCategoriesFileCSV(self.parent.fpathCSV)



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
        self.buttonChangeCategory.setEnabled(True)
        self.buttonDeleteCategory.setEnabled(True)

    def addCategory(self):

        if self.parent.fpathCSV != "" and not self.parent.isJSON:
            newCategorie = self.lineEdit.text()
            self.categories.append(newCategorie)
            # string = ",".join(self.categories)
            with open(self.fpathCSV, "a") as f:
                f.write("," + newCategorie)
        else:
            if self.parent.fpathJSON == "":
                self.parent.fpathJSON = "./ressources/categories.json"
                self.parent.isJSON = True

            newCategorie = self.lineEdit.text()
            self.categories.append(newCategorie)
            data = []
            for c in self.categories:
                temp = {"category": c}
                data.append(temp)
            json_object = json.dumps(data, indent=2)

            with open(self.parent.fpathJSON, "w") as outfile:
                outfile.write(json_object)

        self.loadCategories()

    def deleteCategory(self):
        if self.listView.selectedIndexes():
            selectedCategorie = self.listView.currentIndex().data()
            self.categories.remove(selectedCategorie)

            self.loadCategoriesCSVJson()

            AnnotateManager.deleteAnnotation(selectedCategorie)

            self.loadCategories()

    def changeCategory(self):
        """for e in self.listView.selectionModel().selectedIndexes():
            list.append(self.listView.selectionModel().itemFromIndex(index).text())"""
        if self.listView.selectedIndexes():
            selectedCategorie = self.listView.currentIndex().data()
            idx = int(str(self.listView.currentIndex()).replace("<PySide6.QtCore.QModelIndex(", '')[0])
            oldCat = self.categories[idx]
            self.categories[idx] = selectedCategorie
            self.loadCategoriesCSVJson()

            AnnotateManager.changeAnnotation(selectedCategorie, oldCat)
            self.loadCategories()

    def loadCategoriesCSVJson(self):
        if self.parent.fpathCSV != "" and not self.parent.isJSON:
            string = ",".join(self.categories)
            with open(self.parent.fpathCSV, "w+") as f:
                f.write(string)

        if self.parent.fpathJSON != "" and self.parent.isJSON:
            # self.categories.remove(selectedCategorie)
            data = []
            for c in self.categories:
                temp = {"category": c}
                data.append(temp)
            json_object = json.dumps(data, indent=2)

            with open(self.parent.fpathJSON, "w") as outfile:
                outfile.write(json_object)

    def loadCategories(self):
        self.model.clear()
        for category in self.categories:
            item = QStandardItem(category)
            item.setEditable(True)
            self.model.appendRow(item)

    def loadCategoriesFileCSV(self, fpathCSV):
        if fpathCSV != "":
            self.parent.fpathCSV = fpathCSV
            self.parent.isJSON = False
            self.parent.fpathJSON = ""
            fd = open(fpathCSV)
            lines = " ".join(fd.readlines())
            cat = lines.split(",")

            self.categories = cat
            self.loadCategories()

    def loadCategoriesFileJSON(self, fpathJSON):

        if fpathJSON != "":
            self.parent.fpathJSON = fpathJSON
            self.parent.fpathCSV = ""
            self.parent.isJSON = True
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
