import sys, random
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QGraphicsView, QMainWindow, QApplication, QLabel, QVBoxLayout, QStatusBar
from PySide6.QtGui import QAction



class ImageAnnotator(QtWidgets.QWidget):

    def __init__(self):
        super(ImageAnnotator, self).__init__()
        self.title = "ImageAnnotator"
        self.setWindowTitle(self.title)
        self.setFixedSize(QSize(1280, 720))
        # self.resize(1280, 720)
        # self.loadImage()


        self.button = QtWidgets.QPushButton("Load files")
        self.label = QLabel(self)

        self.layout: QVBoxLayout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignBottom)
        self.dialog = QFileDialog(self, "Open Image", filter="Images (*.png *.xpm *.jpg)")
        self.dialog.setFileMode(QFileDialog.AnyFile)

        self.button.clicked.connect(self.loadFile)
        self.fileName = None

        self.menue = MenueBar()
        self.layout.addWidget(self.menue)

    @QtCore.Slot()
    def magic(self):
        self.loadImage()

    @QtCore.Slot()
    def loadFile(self):
        self.fileName = QFileDialog.getOpenFileName(self)
        self.loadImage()

    def loadImage(self):
        fPath = self.fileName[0]
        if fPath != "":
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
            pixmap = QPixmap(fPath)

            self.label.setPixmap(pixmap)
            self.label.setFixedSize(self.size())

class MenueBar(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open = QAction("Open", self)
        open.setShortcut("Ctrl+o")
        open.triggered.connect(self.loadFile)
        file_menu.addAction(open)

        save = QAction("Save",self)
        save.setShortcut("Ctrl+s")
        file_menu.addAction(save)

        close = QAction("Close", self)
        #quit.setShortcut("Ctrl+q")
        file_menu.addAction(close)

        file_menu.triggered[QAction].connect(self.processtrigger)

    
    def onMyToolBarButtonClick(self):
        print("click")

    def processtrigger(self,q):
          print(q.text()+" is triggered")

    def loadFile(self):
        self.fileName = QFileDialog.getOpenFileName(self)
        self.loadImage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ImageAnnotator()
    w.show()
    sys.exit(app.exec())