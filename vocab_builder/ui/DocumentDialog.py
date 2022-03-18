from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure import VocabBuilderDB


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
        for word_context in self.__word.get_short_contexts(self.__doc):
            label = QLabel(word_context.context)
            # FIXME highlight word in the context
            vbox.addWidget(label)
            hbox.addLayout(vbox)
        return hbox


    def __get_bottom_bar(self) -> QHBoxLayout:
        # TODO
        return QHBoxLayout()
