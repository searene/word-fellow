from typing import Dict, Optional

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.domain.word.WordValueObject import ShortAndLongContext
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.ContextItemWidget import ContextItemWidget


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
            [item.hide() for item in self.__context_items]
            self.__no_word_available_label.show()
        else:
            short_and_long_contexts = self.word.get_short_and_long_contexts(self.__doc)
            self.__no_word_available_label.hide()
            for i in range(len(short_and_long_contexts)):
                self.__update_and_show_context_item(self.__context_items, i, short_and_long_contexts[i], self.__layout)
            for i in range(len(short_and_long_contexts), len(self.__context_items)):
                self.__context_items[i].hide()

    def __update_and_show_context_item(self, context_items: [ContextItemWidget], item_index: int,
                                       short_and_long_context: ShortAndLongContext, layout: QVBoxLayout) -> None:
        if len(context_items) <= item_index:
            # create a new context item
            context_item = ContextItemWidget(short_and_long_context)
            layout.addWidget(context_item)
            context_items.append(context_item)
        else:
            context_items[item_index].update_layout(short_and_long_context)
            context_items[item_index].show()

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
        self.__context_items: [ContextItemWidget] = []
        self.__no_word_available_label = self.__get_no_word_available_label()
        vbox.addWidget(self.__no_word_available_label)
        if word is None:
            self.__no_word_available_label.show()
            self.setLayout(vbox)
            return vbox
        self.__no_word_available_label.hide()
        for short_and_long_context in word.get_short_and_long_contexts(doc):
            context_item = ContextItemWidget(short_and_long_context)
            vbox.addWidget(context_item)
            self.__context_items.append(context_item)
        self.setLayout(vbox)
        return vbox

    def __get_no_word_available_label(self) -> QLabel:
        return QLabel("No word is available")