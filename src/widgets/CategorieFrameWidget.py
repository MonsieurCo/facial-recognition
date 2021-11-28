from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor


class CategorieFrame(QtWidgets.QWidget):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent)
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
        self.setLayout(self.layout)

    def validate(self):
        print(self.categories[self.itemSelectedIndex])
        self._close()

    def _close(self):
        self.close()

    def onItemSelected(self, index):
        item = self.model.itemFromIndex(index)
        self.itemSelectedIndex = item.row()
        item.setForeground(QBrush(QColor(255, 0, 0)))
        self.oldItem.setForeground(QColor(255, 255, 255))
        self.oldItem = item

