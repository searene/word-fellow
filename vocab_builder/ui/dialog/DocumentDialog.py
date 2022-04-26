from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QApplication

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.status.GlobalWordStatus import upsert_word_status, Status
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.ContextList import ContextList
from aqt import mw
from aqt.utils import tooltip


class DocumentDialog(QDialog):

    def __init__(self, doc: Document, db: VocabBuilderDB):
        super(DocumentDialog, self).__init__()
        self.__db = db
        self.__doc = doc
        self.__offset = 0
        self.__status_combo_box = self.__get_status_combo_box()
        word_status = self.__get_word_status()
        self.__context_list = self.__get_context_list(self.__doc, word_status, db)
        self.__middle_area_hbox = self.__get_middle_area(self.__context_list)
        self.__dialog_layout = self.__get_dialog_layout(self.__middle_area_hbox)
        self.__init_ui(self.__dialog_layout)

    def show_dialog(self):
        self.show()
        self.exec_()

    def close_dialog(self):
        self.close()

    def __get_dialog_layout(self, middle_area_hbox: QHBoxLayout) -> QVBoxLayout:
        vbox = QVBoxLayout()
        vbox.addLayout(self.__get_top_bar())
        vbox.addLayout(middle_area_hbox)
        vbox.addLayout(self.__get_bottom_bar())
        return vbox

    def __init_ui(self, dialog_layout: QVBoxLayout):
        self.setWindowTitle(self.__doc.name)
        self.setLayout(dialog_layout)

    def __get_top_bar(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(self.__status_combo_box)
        return hbox

    def __get_status_combo_box(self) -> QComboBox:
        status_combo_box = QComboBox()
        for status in WordStatus:
            status_combo_box.addItem(status.name)
        status_combo_box.currentTextChanged.connect(self.__on_status_selected)
        return status_combo_box

    def __on_status_selected(self, status_name: str) -> None:
        status = WordStatus[status_name]
        self.__context_list.update_status(status)

    def __get_word_status(self) -> WordStatus:
        return WordStatus[self.__status_combo_box.currentText()]

    def __get_context_list(self, doc: Document, status: WordStatus, db: VocabBuilderDB) -> ContextList:
        context_list = ContextList(doc, status, db)
        return context_list

    def __get_middle_area(self, context_list: ContextList) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(context_list)
        return hbox

    def __get_bottom_bar(self) -> QHBoxLayout:
        res = QHBoxLayout()

        res.addWidget(self.__get_add_to_anki_btn())

        close_btn = QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.close_dialog)
        res.addWidget(close_btn)

        # TODO Add other buttons

        return res

    def __get_add_to_anki_btn(self) -> QPushButton:
        add_to_anki_btn = QPushButton("Add to anki")
        add_to_anki_btn.clicked.connect(lambda: self.__on_add_to_anki())
        return add_to_anki_btn

    def __on_add_to_anki(self) -> None:
        mw.onAddCard()
        QApplication.clipboard().setText(self.__context_list.word.text)
        tooltip("The word has been copied into the clipboard.", 3000)

        # Set the word status to STUDYING
        upsert_word_status(self.__context_list.word.text, Status.STUDYING, self.__db)

        self.__context_list.next_page()