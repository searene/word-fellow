from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.domain.word.WordValueObject import WordContext
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.LongContextDialog import LongContextDialog
from vocab_builder.ui.util import WordUtils


class DocumentDialog(QDialog):

    def __init__(self, doc: Document, db: VocabBuilderDB):
        super(DocumentDialog, self).__init__()
        self.__db = db
        self.__doc = doc
        self.__offset = 0
        self.__status_combo_box = DocumentDialog.__get_status_combo_box()
        self.__word = doc.get_next_word(0, self.__get_word_status(), db)
        self.__init_ui()

    def show_dialog(self):
        self.show()
        self.exec_()

    def close_dialog(self):
        self.close()

    def __init_ui(self):
        self.setWindowTitle(self.__doc.name)

        vbox = QVBoxLayout()
        vbox.addLayout(self.__get_top_bar())
        vbox.addLayout(self.__get_middle_area())
        vbox.addLayout(self.__get_bottom_bar())
        self.setLayout(vbox)

    def __get_top_bar(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(self.__status_combo_box)
        return hbox

    @staticmethod
    def __get_status_combo_box() -> QComboBox:
        status_combo_box = QComboBox()
        for status in WordStatus:
            status_combo_box.addItem(status.name)
        return status_combo_box

    def __get_word_status(self) -> WordStatus:
        return WordStatus[self.__status_combo_box.currentText()]

    def __get_middle_area(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        if self.__word is None:
            hbox.addWidget(QLabel("No word is available"))
            return hbox
        vbox = QVBoxLayout()
        for short_and_long_context in self.__word.get_short_and_long_contexts(self.__doc):

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
            hbox.addLayout(vbox)
        return hbox

    def __show_long_context_dialog(self, long_context: WordContext) -> None:
        long_context_dialog = LongContextDialog(long_context)
        long_context_dialog.show_dialog()

    def __get_bottom_bar(self) -> QHBoxLayout:
        res = QHBoxLayout()

        close_btn = QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.close_dialog)
        res.addWidget(close_btn)

        # TODO Add other buttons

        return res
