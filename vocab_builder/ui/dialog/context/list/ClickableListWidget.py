from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QListWidget


class ClickableListWidget(QListWidget):
    """This is a custom QListWidget that shows the cursor when the user hovers over an item."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """Set the cursor to hand when the mouse hovers over an item in it."""
        super().mouseMoveEvent(e)
        if self.itemAt(e.pos()) is not None:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
