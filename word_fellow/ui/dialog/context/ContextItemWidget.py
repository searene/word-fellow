from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLayout, QListWidgetItem

from ....domain.word.WordValueObject import ShortAndLongContext


class ContextItemWidget(QtWidgets.QWidget):

    def __init__(self, short_and_long_context: ShortAndLongContext):
        super(ContextItemWidget, self).__init__()
        self.__short_and_long_context = short_and_long_context
        self.short_html = short_and_long_context.short.to_html(allow_multi_line=False)
        self.__layout = self.__get_layout(self.short_html)
        self.item = self.__get_item(short_and_long_context)
        self.setLayout(self.__layout)

    def __get_layout(self, short_html: str) -> QHBoxLayout:
        label = QLabel(short_html)
        label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        widget_layout = QHBoxLayout()
        widget_layout.addWidget(label)
        widget_layout.setSizeConstraint(QLayout.SetFixedSize)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        return widget_layout

    def __get_item(self, short_and_long_context: ShortAndLongContext) -> QListWidgetItem:
        item = QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, short_and_long_context.long)
        item.setHidden(False)
        return item
