import uuid
from typing import Optional

import PySide6.QtGui
from PIL import Image
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPixmap, QMouseEvent, QScreen
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGraphicsView, QApplication, QGraphicsRectItem, QGraphicsScene
from shapely.geometry import Polygon

import src.widgets.CategorieFrameWidget as CategorieFrameWidget
from src import AnnotateManager
from src.widgets import rects


class MyRect(QGraphicsRectItem):
    def __init__(self, fPath: str, brush: QtGui.QBrush, size, choice: str, scene: QGraphicsScene,
                 parent: Optional[PySide6.QtWidgets.QGraphicsItem] = ..., oldId: str = "") -> None:
        super().__init__(parent)
        self.normalized = self.rect().normalized()
        self.fPath = fPath
        self.parent = parent
        self.size = size
        self.choice = choice
        self.setBrush(brush)
        self.setOpacity(0.25)
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        self.scene = scene
        self.label = QtWidgets.QLabel()
        self.rectId = oldId if len(oldId) else str(uuid.uuid4())
        self.label.move(self.normalized.bottomRight().x(),
                        self.normalized.bottomRight().y())
        self.label.setStyleSheet("QLabel { color:" + brush.color().name() + " }")
        self.label.setText(choice)
        self.view = None

    def mouseDoubleClickEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)
        frame = CategorieFrameWidget.CategorieFrame(self.fPath,
                                                    self.normalized.topLeft(),
                                                    self.normalized.bottomRight(),
                                                    self,
                                                    self.size,
                                                    self.scene,
                                                    parent=self.parent,
                                                    isEditing=True)
        frame.show()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.buttons() & QtCore.Qt.RightButton:
            self.Xbegin = self.normalized.topLeft().x()
            self.Ybegin = self.normalized.topLeft().y()
            AnnotateManager.deleteAnnotationByCoord(self.Xbegin, self.Ybegin)

            idx = rects.RECTS[self.fName].index(self)
            self.scene.removeItem(self)
            del rects.RECTS[self.fName][idx]


class View(QGraphicsView):
    def __init__(self, fPath: str, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        self.pScene: QGraphicsScene = parent.getScene()
        super().__init__(self.pScene)
        self.fPath = fPath
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        rects.RECTS[self.fName] = []
        self.parent = parent
        self.begin = QtCore.QPoint()
        self.destination = QtCore.QPoint()
        self.setupImage()
        self.pixmap = QPixmap(self.fPath)
        self.pScene.addPixmap(self.pixmap)
        self.currentRect: QtWidgets.QGraphicsRectItem = None
        self.frame = None
        # self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imgSize = (self.pixmap.width(), self.pixmap.height())

        self.rectsToRemove = []
        self.indexesAnnotation = []

    def getImgSize(self):
        return self.imgSize

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        if event.buttons() & QtCore.Qt.LeftButton:
            self.begin = event.pos()
            # self._update(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if event.buttons() & QtCore.Qt.LeftButton:
            self._update(event)

    def isValidRect(self):
        if self.currentRect is None or \
                self.currentRect.rect().width() < 5 or \
                self.currentRect.rect().height() < 5:
            return False

        normalizedRect = self.currentRect.rect().normalized()
        p = Polygon([
            (normalizedRect.topLeft().x(), normalizedRect.topLeft().y()),
            (normalizedRect.topRight().x(), normalizedRect.topRight().y()),
            (normalizedRect.bottomRight().x(), normalizedRect.bottomRight().y()),
            (normalizedRect.bottomLeft().x(), normalizedRect.bottomLeft().y())
        ])

        if p.area < 40:
            return False

        for i, rect in enumerate(rects.RECTS[self.fName]):
            currentNormalizedRect = rect.rect().normalized()
            currentP = Polygon([
                (currentNormalizedRect.topLeft().x(), currentNormalizedRect.topLeft().y()),
                (currentNormalizedRect.topRight().x(), currentNormalizedRect.topRight().y()),
                (currentNormalizedRect.bottomRight().x(), currentNormalizedRect.bottomRight().y()),
                (currentNormalizedRect.bottomLeft().x(), currentNormalizedRect.bottomLeft().y())
            ])
            p3 = p.intersection(currentP)
            surface = p3.area / currentP.area * 100

            if currentP.contains(p):
                self.pScene.removeItem(self.currentRect)
                return False
            if surface >= 20:
                self.rectsToRemove.append(rect)

        return True

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        if event.button() & QtCore.Qt.LeftButton:
            self.pScene.removeItem(self.currentRect)
            if self.isValidRect():
                self.currentRect = MyRect(self.fPath,
                                          QtGui.QBrush(Qt.black),
                                          (self.pScene.width(), self.pScene.height()),
                                          "", self.pScene,
                                          QRect(self.begin, self.destination).normalized())
                # self.setStyle(QtGui.QBrush())
                self.pScene.addItem(self.currentRect)
                self.frame = CategorieFrameWidget.CategorieFrame(self.fPath,
                                                                 self.begin,
                                                                 self.destination,
                                                                 self.currentRect,
                                                                 self.getImgSize(),
                                                                 self.pScene,
                                                                 parent=self.parent)
                self.frame.show()
            self.currentRect = None
            self.begin, self.destination = QPoint(), QPoint()

    def _update(self, event: QMouseEvent):
        if self.currentRect is not None:
            self.pScene.removeItem(self.currentRect)
        self.destination = event.pos()
        if self.begin.isNull() or self.destination.isNull():
            self.begin = QPoint()
            self.destination = QPoint()
            return
        self.currentRect = MyRect(
            self.fPath,
            QtGui.QBrush(Qt.black),
            (self.pScene.width(), self.pScene.height()),
            "", self.pScene,
            QRect(self.begin, self.destination).normalized())
        self.pScene.addItem(self.currentRect)

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
            self.fPath = splitFPath[0] + "." + splitFPath[1]
            im.save(self.fPath)
        self.resize(newWidth, newHeight)
        self.setFixedSize(self.size())

    def getParent(self):
        return self.parent
