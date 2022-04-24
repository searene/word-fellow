from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.domain.word.WordValueObject import WordContext
from vocab_builder.ui.dialog.LongContextDialog import LongContextDialog
from vocab_builder.ui.util import WordUtils


class ContextList(QtWidgets.QWidget):

    def __init__(self, word: Word, doc: Document, status: WordStatus):
        super(ContextList, self).__init__()

        self.__init_ui(word, doc, status)

    def __init_ui(self, word: Word, doc: Document, status: WordStatus):
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

