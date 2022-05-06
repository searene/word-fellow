from typing import Dict, Optional

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QAbstractItemView

from word_fellow.domain.document.Document import Document
from word_fellow.domain.word.Word import Word
from word_fellow.domain.word.WordStatus import WordStatus
from word_fellow.domain.word.WordValueObject import ShortAndLongContext, WordContext
from word_fellow.infrastructure import WordFellowDB
from word_fellow.ui.dialog.context.ContextItemWidget import ContextItemWidget
from word_fellow.ui.dialog.LongContextDialog import LongContextDialog
from word_fellow.ui.dialog.context.list.ClickableListWidget import ClickableListWidget


class ContextListWidget(QtWidgets.QWidget):

    def __init__(self, word: Optional[Word], doc: Document, status: WordStatus, db: WordFellowDB, status_to_offset_dict: Dict[WordStatus, int]):
        super(ContextListWidget, self).__init__()
        self.__doc = doc
        self.__status = status
        self.__db = db
        self.__status_to_offset_dict = status_to_offset_dict
        self.__word = word
        self.__layout = self.__init_ui(self.__word, doc)

    def set_word(self, word: Optional[Word]):
        self.__word = word

    def set_status(self, status: WordStatus):
        self.__status = status

    def get_item_htmls(self) -> [str]:
        return [item.short_html for item in self.__list_items]

    def update_data(self):
        self.__clear_list_widget(self._list_widget, self.__list_items)
        if self.__word is None:
            self._list_widget.hide()
            self.__no_word_available_label.show()
        else:
            short_and_long_contexts = self.__word.get_short_and_long_contexts(self.__doc)
            self.__no_word_available_label.hide()
            self._list_widget.show()
            for i in range(len(short_and_long_contexts)):
                self.__list_items.append(self.__add_item_to_list_widget(self._list_widget, short_and_long_contexts[i]))

    def __clear_list_widget(self, list_widget: QListWidget, items: [ContextItemWidget]) -> None:
        item_count = len(items)
        for i in range(item_count):
            items.pop(0)
            list_widget.takeItem(0)

    def __get_word(self, doc: Document, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int],
                   db: WordFellowDB) -> Optional[Word]:
        offset = self.__get_offset(status, status_to_offset_dict)
        return doc.get_next_word(offset, status, db)

    def __get_offset(self, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int]) -> int:
        if status not in status_to_offset_dict:
            status_to_offset_dict[status] = 0
        return status_to_offset_dict[status]

    def __init_ui(self, word: Optional[Word], doc: Document) -> QVBoxLayout:
        vbox = QVBoxLayout()

        self._list_widget = ClickableListWidget()
        self._list_widget.itemClicked.connect(self.__on_item_clicked)
        vbox.addWidget(self._list_widget)

        self.__no_word_available_label = self.__get_no_word_available_label()
        vbox.addWidget(self.__no_word_available_label)

        self.__list_items: [ContextItemWidget] = []

        if word is None:
            self._list_widget.hide()
        else:
            self.__no_word_available_label.hide()
            for item_index, short_and_long_context in list(enumerate(word.get_short_and_long_contexts(doc))):
                item = self.__add_item_to_list_widget(self._list_widget, short_and_long_context)
                self.__list_items.append(item)

        self.setLayout(vbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        return vbox

    def __on_item_clicked(self, item: QListWidgetItem) -> None:
        long_context: WordContext = item.data(QtCore.Qt.UserRole)
        long_context_dialog = LongContextDialog(long_context)
        long_context_dialog.show_dialog()

    def __add_item_to_list_widget(self, list_widget: QListWidget, short_and_long_context: ShortAndLongContext) -> ContextItemWidget:
        context_item = ContextItemWidget(short_and_long_context)
        list_widget.addItem(context_item.item)
        list_widget.setItemWidget(context_item.item, context_item)
        return context_item

    def __get_no_word_available_label(self) -> QLabel:
        res = QLabel("No word is available.")
        res.setAlignment(QtCore.Qt.AlignCenter)
        res.setStyleSheet("QLabel { border: 1px solid #B7B7B7; background: white; }")
        return res
