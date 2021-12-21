from typing import Optional

import PySide6.QtGui
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QVBoxLayout

from src import AnnotateManager
from src.QtColors import QtColors
from src.widgets import SelectAreaGraphicSceneWidget, MenuBarWidget
from src.widgets import rects
from src.widgets.SelectAreaGraphicSceneWidget import MyRect


class FrameImage(QtWidgets.QWidget):

    def __init__(self, fPath, name, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent=parent)
        """
        this Class represent the image opened in the software
            

        :param fPath: The image path
        :type fPath: str
        :param name: iamge name 
        :type name:  str
        :returns: a QWidget with a scene in it 
        :rtype: QWidget
        
        
    
        """



        self.frame = None
        self.title = name
        self.setWindowTitle(self.title)

        #     Categories PATH
        self.fpathCSV = ""
        self.fpathJSON = "./ressources/categories.json"
        self.isJSON = True

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)
        self.graphicsView = None
        self.scene = QGraphicsScene(self)
        self.menu = MenuBarWidget.MenuBar(False, self)
        self.layout.setMenuBar(self.menu)
        self.fPath = fPath
        self.name = name
        self.fName = self.fPath.split("/")[-1].split(".")[0]
        self.load()
        self.show()

    def load(self):
        """
        load the image to display it in a new window,
        create a SelectAreaGraphicSceneWidget

        :return:
        """

        if self.graphicsView is not None:
            self.scene.removeItem(self.graphicsView)
        if self.fPath != "":
            self.graphicsView = SelectAreaGraphicSceneWidget.View(self.fPath,
                                                                  parent=self)
            self.scene.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
            self.layout.addWidget(self.graphicsView, alignment=QtCore.Qt.AlignCenter)
            # center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
            # geo = self.frameGeometry()
            # geo.moveCenter(center)
            # self.move(geo.topLeft())
            self.setLayout(self.layout)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        """
        will display the area selected on the image
        :param event:
        :type event:  QtGui.QShowEvent
        :return:
        """
        super().showEvent(event)
        try:
            annotations = AnnotateManager.annotations[self.fName]["annotations"]
            if self.fName not in rects.RECTS:
                rects.RECTS[self.fName] = []
            for annotation in annotations:
                rect = MyRect(self.fPath,
                              QtGui.QBrush(QtColors.COLORS[annotation["categorie_id"] % QtColors.lengthColors]),
                              (self.scene.width(), self.scene.height()),
                              annotation["categorie"], self.scene,
                              parent=QRect(
                                  QPoint(annotation["coords"]["beginX"],
                                         annotation["coords"]["beginY"]),
                                  QPoint(
                                      annotation["coords"]["destinationX"],
                                      annotation["coords"]["destinationY"]
                                  )).normalized(),
                              oldId=annotation["id"]
                              )


                rect.label.setText(annotation["categorie"])
                rect.label.adjustSize()
                rects.RECTS[self.fName].append(rect)
                self.scene.addWidget(rect.label)
                self.scene.addItem(rect)

        except Exception as e:
            pass

    def getScene(self) -> QGraphicsScene:
        """
        :return: the Graphic Scene
        :rtype: QGraphicsScene
        """
        return self.scene

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        """
        close with the event listener inherited
        :param event: closing event
        :type event: PySide6.QtGui.QCloseEvent
        :return:
        """
        super().closeEvent(event)