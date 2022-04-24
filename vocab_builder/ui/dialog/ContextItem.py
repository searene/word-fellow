from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton

from vocab_builder.domain.word.WordValueObject import ShortAndLongContext, WordContext
from vocab_builder.ui.dialog.LongContextDialog import LongContextDialog
from vocab_builder.ui.util import WordUtils


class ContextItem(QtWidgets.QWidget):

    def __init__(self, short_and_long_context: ShortAndLongContext):
        super(ContextItem, self).__init__()
        self.__short_and_long_context = short_and_long_context
        self.__layout = self.__get_layout(short_and_long_context)
        self.setLayout(self.__layout)

    def update_layout(self, short_and_long_context: ShortAndLongContext) -> None:
        self.__label.setText(WordUtils.convert_word_context_to_html(short_and_long_context.short))

        self.__layout.removeWidget(self.__check_more_btn)
        self.__check_more_btn.deleteLater()
        self.__check_more_btn = None
        self.__check_more_btn = self.__get_btn(short_and_long_context.long)
        self.__layout.addWidget(self.__check_more_btn)

    def __get_layout(self, short_and_long_context: ShortAndLongContext) -> QHBoxLayout:
        res = QHBoxLayout()

        # Add a short context label
        self.__label = QLabel(WordUtils.convert_word_context_to_html(short_and_long_context.short))
        res.addWidget(self.__label)

        # Add a button for long contexts
        self.__check_more_btn = self.__get_btn(short_and_long_context.long)
        res.addWidget(self.__check_more_btn)
        return res

    def __get_btn(self, long_context: WordContext) -> QPushButton:
        res = QPushButton("Click for more")
        res.clicked.connect(lambda: self.__show_long_context_dialog(long_context))
        return res

    def __show_long_context_dialog(self, long_context: WordContext) -> None:
        long_context_dialog = LongContextDialog(long_context)
        long_context_dialog.show_dialog()

