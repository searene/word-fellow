from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLineEdit


class ClickableLineEdit(QLineEdit):

    clicked = pyqtSignal()

    def __init__(self, parent):
        super(ClickableLineEdit, self).__init__(parent)
        self.parentWindow = parent

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            ClickableLineEdit.clicked.emit()
        else:
            super().mousePressEvent(event)