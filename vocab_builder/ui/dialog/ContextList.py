from typing import Dict, Optional

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.domain.word.WordValueObject import WordContext
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.LongContextDialog import LongContextDialog
from vocab_builder.ui.util import WordUtils


class ContextList(QtWidgets.QWidget):

    def __init__(self, doc: Document, status: WordStatus, db: VocabBuilderDB):
        super(ContextList, self).__init__()
        self.__doc = doc
        self.__status = status
        self.__db = db
        self.__status_to_offset_dict = {}
        self.__word = self.__get_word(doc, status, self.__status_to_offset_dict, db)
        self.__init_ui(self.__word, doc)

    def update_status(self, status: WordStatus):
        self.__word = self.__get_word(self.__doc, status, self.__status_to_offset_dict, self.__db)
        self.__init_ui(self.__word, self.__doc)

    def __get_word(self, doc: Document, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int],
                   db: VocabBuilderDB) -> Optional[str]:
        offset = self.__get_offset(status, status_to_offset_dict)
        return doc.get_next_word(offset, status, db)

    def __get_offset(self, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int]) -> int:
        if status not in status_to_offset_dict:
            status_to_offset_dict[status] = 0
        return status_to_offset_dict[status]

    def __init_ui(self, word: Optional[Word], doc: Document):
        vbox = QVBoxLayout()
        if word is None:
            vbox.addWidget(QLabel("No word is available"))
            return vbox
        for short_and_long_context in word.get_short_and_long_contexts(doc):
            context_hbox = QHBoxLayout()

            # Add a short context label
            short_context = short_and_long_context.short_context
            long_context = short_and_long_context.long_context
            label = QLabel(WordUtils.convert_word_context_to_html(short_context))
            context_hbox.addWidget(label)

            # Add a button for long contexts
            check_more_btn = QPushButton("Click for more")
            check_more_btn.clicked.connect(lambda: self.__show_long_context_dialog(long_context))
            context_hbox.addWidget(check_more_btn)

            vbox.addLayout(context_hbox)
        self.setLayout(vbox)

    def __show_long_context_dialog(self, long_context: WordContext) -> None:
        long_context_dialog = LongContextDialog(long_context)
        long_context_dialog.show_dialog()
