from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from vocab_builder.domain.word.WordValueObject import ShortAndLongContext, WordContext
from vocab_builder.ui.dialog.LongContextDialog import LongContextDialog
from vocab_builder.ui.util import WordUtils


class ContextItem(QtWidgets.QWidget):

    def __init__(self, short_and_long_context: ShortAndLongContext):
        super(ContextItem, self).__init__()
        self.__short_and_long_context = short_and_long_context
        self.__layout = self.__get_layout(short_and_long_context)
        self.setLayout(self.__layout)

    def __get_layout(self, short_and_long_context: ShortAndLongContext) -> QHBoxLayout:
        res = QHBoxLayout()

        # Add a short context label
        short_context = short_and_long_context.short_context
        long_context = short_and_long_context.long_context
        label = QLabel(WordUtils.convert_word_context_to_html(short_context))
        res.addWidget(label)

        # Add a button for long contexts
        check_more_btn = QPushButton("Click for more")
        check_more_btn.clicked.connect(lambda: self.__show_long_context_dialog(long_context))
        res.addWidget(check_more_btn)
        return res

    def __show_long_context_dialog(self, long_context: WordContext) -> None:
        long_context_dialog = LongContextDialog(long_context)
        long_context_dialog.show_dialog()
