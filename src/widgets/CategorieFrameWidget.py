from typing import Optional

import PySide6.QtWidgets
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

from src import AnnotateManager, Annotation


class CategorieFrame(QtWidgets.QWidget):
    def __init__(self, fPath, coords, parent: Optional[PySide6.QtWidgets.QWidget] = ...) -> None:
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
        self.button = QtWidgets.QPushButton("OK", self)
        self.button.clicked.connect(self.validate)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.listView)
        self.layout.addWidget(self.button)
        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        self.setLayout(self.layout)

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
