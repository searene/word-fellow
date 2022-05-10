from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QListWidget, QAbstractItemView


class ClickableListWidget(QListWidget):
    """This is a custom QListWidget that shows the cursor when the user hovers over an item."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setStyleSheet("QListWidget::item:hover { border-bottom: 1px solid black; }")
        self.setMouseTracking(True)

    # TODO it's not invoked when the cursor is inside the widget at first
    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """Set the cursor to hand when the mouse hovers over an item in it."""
        super().mouseMoveEvent(e)
        if self.itemAt(e.pos()) is not None:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
