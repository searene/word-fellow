from typing import Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QWidget


class ClickableLineEdit(QLineEdit):

    clicked = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super(ClickableLineEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()
