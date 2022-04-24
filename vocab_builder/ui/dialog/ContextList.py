from typing import Dict, Optional

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.ContextItem import ContextItem


class ContextList(QtWidgets.QWidget):

    def __init__(self, doc: Document, status: WordStatus, db: VocabBuilderDB):
        super(ContextList, self).__init__()
        self.__doc = doc
        self.__status = status
        self.__db = db
        self.__status_to_offset_dict = {}
        self.__word = self.__get_word(doc, status, self.__status_to_offset_dict, db)
        self.__layout = self.__init_ui(self.__word, doc)

    def update_status(self, status: WordStatus):
        self.__word = self.__get_word(self.__doc, status, self.__status_to_offset_dict, self.__db)

    def __get_word(self, doc: Document, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int],
                   db: VocabBuilderDB) -> Optional[str]:
        offset = self.__get_offset(status, status_to_offset_dict)
        return doc.get_next_word(offset, status, db)

    def __get_offset(self, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int]) -> int:
        if status not in status_to_offset_dict:
            status_to_offset_dict[status] = 0
        return status_to_offset_dict[status]

    def __init_ui(self, word: Optional[Word], doc: Document) -> QVBoxLayout:
        vbox = QVBoxLayout()
        self.__context_items = []
        if word is None:
            vbox.addWidget(QLabel("No word is available"))
            self.setLayout(vbox)
            return vbox
        for short_and_long_context in word.get_short_and_long_contexts(doc):
            context_item = ContextItem(short_and_long_context)
            vbox.addWidget(context_item)
            self.__context_items.append(context_item)
        self.setLayout(vbox)
        return vbox

