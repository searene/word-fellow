from typing import Dict, Optional

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QLayout, QWidget

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.domain.word.WordValueObject import ShortAndLongContext, WordContext
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.ContextItemWidget import ContextItemWidget
from vocab_builder.ui.dialog.LongContextDialog import LongContextDialog


class ContextListWidget(QtWidgets.QWidget):

    def __init__(self, doc: Document, status: WordStatus, db: VocabBuilderDB):
        super(ContextListWidget, self).__init__()
        self.__doc = doc
        self.__status = status
        self.__db = db
        self.__status_to_offset_dict: Dict[WordStatus, int] = {}
        self.word = self.__get_word(doc, status, self.__status_to_offset_dict, db)
        self.__layout = self.__init_ui(self.word, doc)

    def next_page(self):
        self.__status_to_offset_dict[self.__status] = self.__status_to_offset_dict[self.__status] + 1
        self.__update_ui()

    def update_status(self, status: WordStatus):
        self.__status = status
        self.__update_ui()

    def __update_ui(self):
        self.word = self.__get_word(self.__doc, self.__status, self.__status_to_offset_dict, self.__db)
        if self.word is None:
            self.__list_widget.hide()
            self.__no_word_available_label.show()
        else:
            short_and_long_contexts = self.word.get_short_and_long_contexts(self.__doc)
            self.__no_word_available_label.hide()
            self.__list_widget.show()
            self.__clear_list_widget(self.__list_widget, self.__list_items)
            for i in range(len(short_and_long_contexts)):
                self.__list_items.append(self.__add_item_to_list_widget(self.__list_widget, short_and_long_contexts[i], i))

    def __clear_list_widget(self, list_widget: QListWidget, items: [QListWidgetItem]) -> None:
        item_count = len(items)
        for i in range(item_count):
            list_widget.takeItem(i)
            items.pop()

    def __get_word(self, doc: Document, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int],
                   db: VocabBuilderDB) -> Optional[Word]:
        offset = self.__get_offset(status, status_to_offset_dict)
        return doc.get_next_word(offset, status, db)

    def __get_offset(self, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int]) -> int:
        if status not in status_to_offset_dict:
            status_to_offset_dict[status] = 0
        return status_to_offset_dict[status]

    def __init_ui(self, word: Optional[Word], doc: Document) -> QVBoxLayout:
        vbox = QVBoxLayout()

        self.__list_widget = QListWidget()
        self.__list_widget.itemDoubleClicked.connect(self.__on_item_clicked)
        vbox.addWidget(self.__list_widget)

        self.__no_word_available_label = QLabel("No word is available")
        vbox.addWidget(self.__no_word_available_label)

        self.__list_items: [QListWidgetItem] = []

        if word is None:
            self.__list_widget.hide()
        else:
            self.__no_word_available_label.hide()
            for item_index, short_and_long_context in list(enumerate(word.get_short_and_long_contexts(doc))):
                item = self.__add_item_to_list_widget(self.__list_widget, short_and_long_context, item_index)
                self.__list_items.append(item)

        self.setLayout(vbox)
        return vbox

    def __on_item_clicked(self, item: QListWidgetItem) -> None:
        long_context: WordContext = item.data(QtCore.Qt.UserRole)
        long_context_dialog = LongContextDialog(long_context)
        long_context_dialog.show_dialog()

    def __add_item_to_list_widget(self, list_widget: QListWidget, short_and_long_context: ShortAndLongContext,
                                  item_index: int) -> QListWidgetItem:
        item = QListWidgetItem()

        label = QLabel(short_and_long_context.short.to_html())
        widget_layout = QHBoxLayout()
        widget_layout.addWidget(label)
        widget_layout.setSizeConstraint(QLayout.SetFixedSize)
        widget = QWidget()
        widget.setLayout(widget_layout)

        item.setData(QtCore.Qt.UserRole, short_and_long_context.long)
        item.setSizeHint(widget.sizeHint())
        item.setHidden(False)
        list_widget.insertItem(item_index, item)
        list_widget.setItemWidget(item, widget)
        return item

    def __get_no_word_available_label(self) -> QLabel:
        return QLabel("No word is available")