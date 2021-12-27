import traceback
import webbrowser
from typing import Optional

from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QVBoxLayout, QDialog, QMessageBox

import src.widgets.FrameImageWidget as FrameImageWidget
from src.annotations import AnnotateManager


class MenuBar(QtWidgets.QMenuBar):

    def __init__(self, bopen, parent: Optional[QtWidgets.QWidget] = ...) -> None:
        """
        MenuBar of every window
        :param bopen: True if main window application opened, otherwise False
        :param parent: parent widget
        """
        super().__init__()

        self.parent = parent
        self.frame = parent.frame
        self.fileMenu = self.addMenu("File")
        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)

        if bopen:
            self.open = self.fileMenu.addMenu("Open")

            self.openFile = QAction("Open file", self)
            self.openFile.setShortcut("Ctrl+o")
            self.openFile.triggered.connect(self.loadFile)
            self.open.addAction(self.openFile)

            self.openFold = QAction("Open folder", self)
            self.openFold.setShortcut("Ctrl+Shift+O")
            self.openFold.triggered.connect(self.frame.load)
            self.open.addAction(self.openFold)

        self.save = QAction("Save", self)
        self.save.setShortcut("Ctrl+s")
        self.save.triggered.connect(self.saveAsJson)

        self.fileMenu.addAction(self.save)

        self.close = QAction("Close", self)
        self.close.setShortcut("Ctrl+w")
        self.close.triggered.connect(self.closeImage)
        self.fileMenu.addAction(self.close)


        self.helpMenu = QAction("Help")
        self.helpMenu.setShortcut("Ctrl+h")
        self.helpMenu.triggered.connect(self.help)
        self.addAction(self.helpMenu)

        self.layout.addWidget(self.fileMenu)
        self.setLayout(self.layout)
        self.fileName = None

    def loadFile(self):
        """
        Get the filepath and load the image
        """
        self.fileName = QFileDialog.getOpenFileName(self)
        self.loadImage()

    def loadImage(self):
        """
        Load an image
        """
        fPath = self.fileName[0]
        if fPath != "":
            self.newFrame = FrameImageWidget.FrameImage(fPath, fPath, None)
            # self.newFrame.show()

    def closeImage(self):
        """
        Close the parent frame that contains the image
        """
        if self.parent is not None:
            self.parent.close()

    def saveAsJson(self):
        """
        Save current annotations into a file
        """
        fName = QFileDialog().getSaveFileName(self, filter="JSON (*.json)")
        name = fName[0]
        if name != "":
            try:
                AnnotateManager.exportToJson(name)
                q = QMessageBox(text=f"Successfully saved to {name}")
                q.setIcon(QMessageBox.Question)

            except Exception as e:
                q = QMessageBox(text=f"An error occured\n{traceback.format_exc()}")
                q.setIcon(QMessageBox.Critical)

            q.setWindowTitle("Export annotations to json file")
            q.setStandardButtons(QMessageBox.Close)
            q.exec_()

    def help(self):
        """
        Help button that redirect to the GitHub Readme
        """
        webbrowser.open_new_tab('https://github.com/MonsieurCo/facial-recognition#readme')
