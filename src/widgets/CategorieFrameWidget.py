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
import os

class CategorieFrame(QtWidgets.QMainWindow):
    def __init__(self, fPath, begin: QPoint, destination: QPoint, currentRect: QtWidgets.QGraphicsRectItem,
                 imgSize: tuple[int, int], scene: QtWidgets.QGraphicsScene,
                 parent: Optional[QtWidgets.QWidget] = ..., isEditing=False) -> None:

        """

        :param fPath: image path
        :type fPath: str
        :param begin: begin point
        :type begin: QPoint
        :param destination: end point
        :type destination: QPoint
        :param currentRect: rectangle drawn by user
        :type currentRect: QtWidgets.QGraphicsRectItem
        :param imgSize: size of the image
        :type imgSize: tuple[int, int]
        :param scene: the graphicScene where rectangles are drawn
        :type scene:  QtWidgets.QGraphicsScene
        :param parent: the parent frame of self
        :type parent: Optional[QtWidgets.QWidget] = ...
        :param isEditing: a boolean to know if the reactagle is being eddited or not
        :type isEditing: bool
        """

        super().__init__()
        self.begin = begin

        self.setFocus()

        self.destination = destination
        self.currentRect = currentRect
        self.parent = parent

        if self.currentRect.view is None:
            self.currentRect.view = self.parent

        self.isEditing = isEditing
        self.listView = QListView(self)

        self.lineEdit = QLineEdit()
        self.addCat = QPushButton()
        self.addCat.setText("Ok")
        self.imgSize = imgSize
        # print("PARENT", self.parent)
        self.scene = scene

        self.connect(self.addCat, SIGNAL("clicked()"), self.addCategory)

        self.model = QStandardItemModel(self.listView)

        self.listView.clicked[QtCore.QModelIndex].connect(self.onItemSelected)
        self.listView.setModel(self.model)
        self.itemSelectedIndex = None
        self.oldItem = QStandardItem()

        self.fPath = fPath

        self.fName = self.fPath.split("/")[-1].split(".")[0]

        self.buttonSelectCategory = QtWidgets.QPushButton(icon=QIcon("./ressources/assets/32x32validate.png"),
                                                          text="\tSelect category")
        self.buttonSelectCategory.setEnabled(False)
        self.buttonSelectCategory.clicked.connect(self.validate)

        self.buttonChangeCategory = QtWidgets.QPushButton(  # icon=QIcon("./ressources/assets/32x32delete.png"),
            text="\tChange category")
        self.buttonChangeCategory.setEnabled(False)
        self.buttonChangeCategory.clicked.connect(self.changeCategory)

        self.buttonDeleteCategory = QtWidgets.QPushButton(icon=QIcon("./ressources/assets/32x32delete.png"),
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
        try:
            if self.parent.isJSON and self.parent.fpathJSON != "":
                self.loadCategoriesFileJSON(self.parent.fpathJSON)
            elif not self.parent.isJSON and self.parent.fpathCSV != "":
                self.loadCategoriesFileCSV(self.parent.fpathCSV)
        except:
            self.loadCategoriesFileJSON("./ressources/config/categories.json")

    def validate(self):
        """
        method called when the user validate a choice, it applies the given category on the rectangle and give it a color, write in the JSON.
        :return:
        """
        choice = self.categories[self.itemSelectedIndex]
        color = QtColors.COLORS[self.itemSelectedIndex % QtColors.lengthColors]

        if self.isEditing:
            annotations = AnnotateManager.annotations[self.fName]["annotations"]
            for annotation in annotations:
                if annotation["id"] == self.currentRect.rectId:
                    annotation["categorie"] = choice
                    annotation["categorie_id"] = self.itemSelectedIndex
                    break
            self.currentRect.setBrush(color)
            self.currentRect.label.setStyleSheet("QLabel { color:" + color.name() + " }")

            self.currentRect.label.setText(choice)

            self.currentRect.choice = choice
            self.currentRect.label.adjustSize()



        else:
            self.currentRect.label.setStyleSheet("QLabel { color:" + color.name() + " }")
            self.currentRect.setBrush(color)
            self.currentRect.label.setText(choice)
            self.currentRect.choice = choice

            AnnotateManager.addAnnotation(self.fName,
                                          Annotation(
                                              self.currentRect.rectId,
                                              self.begin,
                                              self.destination,
                                              choice,
                                              os.path.relpath(self.fPath),
                                              self.itemSelectedIndex,
                                              self.imgSize[0],
                                              self.imgSize[1]
                                          ))

            try:
                rects.RECTS[self.fName].append(self.currentRect)
            except:
                rects.RECTS[self.fName] = [self.currentRect]

            self.scene.addItem(self.currentRect)
            self.scene.addWidget(self.currentRect.label)
        self._close()

    def _close(self):
        """
        private method:
        called when close
        :return:
        """
        self.close()

    def onItemSelected(self, index):
        """
        listener when an item in the category list
        it activates the button to edit or validate a category
        :param index:
        :return:
        """
        item = self.model.itemFromIndex(index)
        self.itemSelectedIndex = item.row()
        self.buttonSelectCategory.setEnabled(True)
        self.buttonChangeCategory.setEnabled(True)
        self.buttonDeleteCategory.setEnabled(True)

    def addCategory(self):
        """
        method called when th user add a category, it add it in the category file imported, if no category file is imported it write it in default file.
        :return:
        """

        if self.parent.fpathCSV != "" and not self.parent.isJSON:
            newCategorie = self.lineEdit.text()
            self.categories.append(newCategorie)
            # string = ",".join(self.categories)
            with open(self.fpathCSV, "a") as f:
                f.write("," + newCategorie)
        else:
            if self.parent.fpathJSON == "":
                self.parent.fpathJSON = "./ressources/config/categories.json"
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
        """
        method called when user delete a category, it removes it from the category file imported
        :return:
        """
        if self.listView.selectedIndexes():
            selectedCategorie = self.listView.currentIndex().data()
            self.categories.remove(selectedCategorie)
            self.deleteSquares()

            self.loadCategoriesCSVJson()

            AnnotateManager.deleteAnnotation(selectedCategorie)

            self.loadCategories()

    def changeCategory(self):
        """
        change the category of a rectangle when it is edited
        :return:
        """
        if self.listView.selectedIndexes():
            selectedCategorie = self.listView.currentIndex().data()
            idx = int(str(self.listView.currentIndex()).replace("<PySide6.QtCore.QModelIndex(", '')[0])
            oldCat = self.categories[idx]
            self.categories[idx] = selectedCategorie
            self.loadCategoriesCSVJson()

            AnnotateManager.changeAnnotation(selectedCategorie, oldCat)
            self.loadCategories()
            for i, rect in enumerate(rects.RECTS[self.fName]):
                annotation = AnnotateManager.annotations[self.fName]["annotations"][i]
                if annotation["id"] ==  rect.rectId:
                    rect.choice = annotation["categorie"]
                    rect.label.setText(annotation["categorie"])
                    rect.label.adjustSize()

    def loadCategoriesCSVJson(self):
        """
        load a category from the path edited by the dialog
        :return:
        """
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
        """
        update categories
        :return:
        """
        self.model.clear()
        for category in self.categories:
            item = QStandardItem(category)
            item.setEditable(True)
            self.model.appendRow(item)

    def loadCategoriesFileCSV(self, fpathCSV):
        """
        load a category from a specific file path
        :param fpathCSV:
        :type fpathCSV: str
        :return:
        """
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
        """
            load a category from a specific file path
            :param fpathJSON:
            :type fpathJSON: str
            :return:
            """
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
        """
        Event when the user close the category frame widget
        make the image enable when this category frame is closed.
        If nothing is selected the rectangle is removed from the image,
        if the rectangle is cover some other rectangle it deletes the rectangles behind if it's validated.
        :param event: closing event
        :type event: PySide6.QtGui.QCloseEvent
        :return:
        """

        try:
            self.currentRect.view.setDisabled(False)
            if not self.currentRect in rects.RECTS[self.fName]:
                self.scene.removeItem(self.currentRect)
            elif self.parent.graphicsView.rectsToRemove != []:
                for i in range(len(self.parent.graphicsView.rectsToRemove)):
                    self.parent.graphicsView.rectsToRemove[i].label.hide()
                    self.scene.removeItem(self.parent.graphicsView.rectsToRemove[i])
                    try:
                        idx = rects.RECTS[self.parent.fName].index(self.parent.graphicsView.rectsToRemove[i])
                        del AnnotateManager.annotations[self.parent.fName]["annotations"][idx]
                        del rects.RECTS[self.parent.fName][idx]
                    except ValueError:
                        pass
                self.parent.graphicsView.rectsToRemove = []
                self.parent.graphicsView.indexesAnnotation = []
        except:
            pass

    def deleteSquares(self):
        """
        method called when the right click is clicked on the rectangle.
        :return:
        """
        if self.fName not in rects.RECTS:
            rects.RECTS[self.fName] = []

        rectsToRemove = []
        for i, rect in enumerate(rects.RECTS[self.fName]):
            annotation = AnnotateManager.annotations[self.fName]["annotations"][i]

            if annotation["categorie"] not in self.categories:
                rectsToRemove.append(rect)

        for i in range(len(rectsToRemove)):
            idx = rects.RECTS[self.fName].index(rectsToRemove[i])
            self.scene.removeItem(rectsToRemove[i])
            rectsToRemove[i].label.hide()
            del rects.RECTS[self.fName][idx]
