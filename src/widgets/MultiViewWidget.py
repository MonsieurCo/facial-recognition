from typing import Optional

import PySide6.QtWidgets
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QDir, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QFileDialog, QVBoxLayout, QListWidget, QListWidgetItem

from src.widgets.FrameImageWidget import FrameImage


class MyListWidget(QListWidget):

    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent)
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(125, 125))
        self.setResizeMode(QListWidget.Adjust)
        self.paths = {}

    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        try:
            super().mouseDoubleClickEvent(event)
            name = self.selectedItems()[0].text()
            frame = FrameImage(self.paths[name], name, None)
        except:
            pass

    def addMyItem(self, item: PySide6.QtWidgets.QListWidgetItem, path: str):
        item.setSizeHint(QSize(150, 150))
        item.setTextAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        super().addItem(item)
        self.paths[item.text()] = path


class MultiView(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.pixmap = QPixmap("./ressources/DRAGNDROP.png")
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)
        self.listWidget = None

    def load(self):
        dirPath = QFileDialog.getExistingDirectory(self)
        self.loadFolder(dirPath)

    def loadFolder(self, dirPath):
        if self.listWidget is not None:
            self.layout.removeWidget(self.listWidget)
        self.listWidget = MyListWidget(None)
        self.layout.removeWidget(self.label)

        directory = QDir(dirPath)
        filtered = ["*.png", "*.xpm", "*.jpg"]
        directory.setNameFilters(filtered)

        for i, file in enumerate(directory.entryList(), start=1):
            self.listWidget.addMyItem(QListWidgetItem(QIcon(f"{dirPath}/{file}"), f"image-{i}"), f"{dirPath}/{file}")

        self.layout.addWidget(self.listWidget)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        url = e.mimeData().urls()[0]
        path = url.toLocalFile()
        if path[-4:] == ".png" or path[-4:] == ".xpm" or path[-4:] == ".jpg":
            frame = FrameImage(path, path, None)
            # frame.show()
        else:
            self.loadFolder(path)
