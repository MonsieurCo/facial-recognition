from PySide6 import QtGui
from PySide6.QtGui import Qt


class QtColors(object):
    """
    Class that contains rectangle categories color
    """
    COLORS = [
        QtGui.QColor(Qt.white),
        QtGui.QColor(Qt.blue),
        QtGui.QColor(Qt.red),
        QtGui.QColor(Qt.green),
        QtGui.QColor(Qt.cyan),
        QtGui.QColor(Qt.yellow),
        QtGui.QColor(Qt.magenta),
        QtGui.QColor(Qt.darkRed),
        QtGui.QColor(Qt.darkGreen),
        QtGui.QColor(Qt.darkBlue),
        QtGui.QColor(Qt.darkCyan),
        QtGui.QColor(Qt.darkMagenta),
        QtGui.QColor(Qt.darkYellow)
    ]
    lengthColors = len(COLORS)
