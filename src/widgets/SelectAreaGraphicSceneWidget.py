from typing import Optional

import PySide6.QtGui
from PIL import Image
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPixmap, QMouseEvent, QScreen
from PySide6.QtWidgets import QGraphicsView, QApplication
from shapely.geometry import Polygon

import src.widgets.CategorieFrameWidget as CategorieFrameWidget
from src import RECTS


class View(QGraphicsView):
    def __init__(self, fPath: str, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent.getScene())
        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        RECTS[self.fName] = []
        self.parent = parent
        self.begin = QtCore.QPoint()
        self.destination = QtCore.QPoint()
        self.setupImage()
        self.pixmap = QPixmap(self.fPath)
        self.pixmapItem = QtWidgets.QGraphicsPixmapItem(self.pixmap)
        self.parent.getScene().addItem(self.pixmapItem)
        self.currentRect: QtWidgets.QGraphicsRectItem = None
        self.frame = None
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)
        try:
            for rect in RECTS[self.fName]:
                normalizedRect = rect.rect().normalized()
                if normalizedRect.contains(event.pos()):
                    self.frame = CategorieFrameWidget.CategorieFrame(self.fPath,
                                                                     normalizedRect.topLeft(),
                                                                     normalizedRect.bottomRight(),
                                                                     rect,
                                                                     self,
                                                                     True)
                    self.frame.show()
        except:
            pass

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.buttons() & QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self._update(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._update(event)

    def isValidRect(self):
        if self.currentRect is None:
            return False

        normalizedRect = self.currentRect.rect().normalized()
        p = Polygon([
            (normalizedRect.topLeft().x(), normalizedRect.topLeft().y()),
            (normalizedRect.topRight().x(), normalizedRect.topRight().y()),
            (normalizedRect.bottomRight().x(), normalizedRect.bottomRight().y()),
            (normalizedRect.bottomLeft().x(), normalizedRect.bottomLeft().y())
        ])
        for rect in RECTS[self.fName]:
            currentNormalizedRect = rect.rect().normalized()
            currentP = Polygon([
                (currentNormalizedRect.topLeft().x(), currentNormalizedRect.topLeft().y()),
                (currentNormalizedRect.topRight().x(), currentNormalizedRect.topRight().y()),
                (currentNormalizedRect.bottomRight().x(), currentNormalizedRect.bottomRight().y()),
                (currentNormalizedRect.bottomLeft().x(), currentNormalizedRect.bottomLeft().y())
            ])
            if p.intersects(currentP):
                return False

        return self.currentRect.rect().size().width() >= 40 \
               and self.currentRect.rect().size().height() >= 40

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() & QtCore.Qt.LeftButton:
            self.parent.getScene().removeItem(self.currentRect)
            if self.isValidRect():
                self.currentRect = QtWidgets.QGraphicsRectItem(
                    QRect(self.begin, self.destination).normalized())
                self.parent.getScene().addItem(self.currentRect)
                self.frame = CategorieFrameWidget.CategorieFrame(self.fPath,
                                                                 self.begin,
                                                                 self.destination,
                                                                 self.currentRect,
                                                                 self.parent)
                self.frame.show()
            self.currentRect = None
            self.begin, self.destination = QPoint(), QPoint()

    def _update(self, event: QMouseEvent):
        if self.currentRect is not None:
            self.parent.getScene().removeItem(self.currentRect)
        self.destination = event.pos()
        self.currentRect = QtWidgets.QGraphicsRectItem(QRect(self.begin, self.destination).normalized())
        self.parent.getScene().addItem(self.currentRect)

    def setupImage(self):
        resize = False
        im: Image = Image.open(self.fPath)
        primaryScreenSize = QScreen.availableGeometry(QApplication.primaryScreen())

        width, height = primaryScreenSize.width(), primaryScreenSize.height()
        newWidth, newHeight = im.size
        if newWidth > width or newHeight > height:
            resize = True

        newWidth = min(newWidth, width)
        newHeight = min(newHeight, height)
        if resize:
            newWidth -= 20
            newHeight -= 70
            im = im.resize((newWidth, newHeight))
            splitFPath = self.fPath.split(".")
            self.fPath = splitFPath[0] + "-resized" + "." + splitFPath[1]
            im.save(self.fPath)
        self.resize(newWidth, newHeight)
        self.setFixedSize(self.size())

    def getParent(self):
        return self.parent
