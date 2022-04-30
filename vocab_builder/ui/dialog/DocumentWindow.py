from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QApplication, QWidget, \
    QSizePolicy, QSpacerItem
from anki.notes import Note

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.status.GlobalWordStatus import upsert_word_status, Status
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.ContextListWidget import ContextListWidget
from aqt import mw
from aqt.utils import tooltip
from aqt import gui_hooks


class DocumentWindow(QWidget):

    def __init__(self, doc: Document, db: VocabBuilderDB):
        super(DocumentWindow, self).__init__()
        self.__db = db
        self.__doc = doc
        self.__offset = 0
        self._status_combo_box = self.__get_status_combo_box()
        self.__status = WordStatus(self._status_combo_box.currentText())
        self._context_list = self.__get_context_list(self.__doc, self.__status, db)
        self.__dialog_layout = self.__get_dialog_layout(self._context_list)
        self.__init_ui(self.__dialog_layout)
        gui_hooks.add_cards_did_add_note.append(self.__raise)
        self.showMaximized()

    def closeEvent(self, event: QCloseEvent) -> None:
        gui_hooks.add_cards_did_add_note.remove(self.__raise)

    def __raise(self, note: Note):
        self.raise_()

    def __get_dialog_layout(self, context_list: ContextListWidget) -> QVBoxLayout:
        vbox = QVBoxLayout()
        vbox.addLayout(self.__get_top_bar())
        vbox.addWidget(context_list)
        vbox.addLayout(self.__get_bottom_bar(context_list))
        return vbox

    def __init_ui(self, dialog_layout: QVBoxLayout):
        self.setWindowTitle(self.__doc.name)
        self.setLayout(dialog_layout)

    def __get_top_bar(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        status_label = QLabel("Status")
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        status_label.setSizePolicy(size_policy)
        hbox.addWidget(status_label)
        hbox.addWidget(self._status_combo_box)
        return hbox

    def __get_status_combo_box(self) -> QComboBox:
        status_combo_box = QComboBox()
        for status in WordStatus:
            status_combo_box.addItem(status.value)
        status_combo_box.currentTextChanged.connect(self.__on_status_selected)
        return status_combo_box

    def __on_status_selected(self, status_value: str) -> None:
        self.__status = WordStatus(status_value)
        self._context_list.update_status(self.__status)
        self.__update_ui()

    def __get_context_list(self, doc: Document, status: WordStatus, db: VocabBuilderDB) -> ContextListWidget:
        context_list = ContextListWidget(doc, status, db)
        return context_list

    def __get_middle_area(self, context_list: ContextListWidget) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(context_list)
        return hbox

    def __get_bottom_bar(self, context_list: ContextListWidget) -> QHBoxLayout:
        res = QHBoxLayout()

        # TODO It gives me an illusion that I'm operating on the selected item in the list
        # Maybe we shouldn't let the user select in the list, we only let the user click
        # TODO Add button tips
        self._add_to_anki_btn = self.__get_add_to_anki_btn()
        self._ignore_btn = self.__get_ignore_btn()
        self._know_btn = self.__get_know_btn()
        self._study_later_btn = self.__get_study_later_btn()
        res.addWidget(self._add_to_anki_btn)
        res.addWidget(self._ignore_btn)
        res.addWidget(self._know_btn)
        res.addWidget(self._study_later_btn)
        res.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # TODO set the button to be disabled if there is no prev/next page
        self._prev_page_btn = self.__get_prev_page_btn()
        self._next_page_btn = self.__get_next_page_btn(context_list)
        res.addWidget(self._prev_page_btn)
        res.addWidget(self._next_page_btn)

        return res

    def __get_prev_page_btn(self) -> QPushButton:
        btn = QPushButton("<")
        btn.setDisabled(True)
        btn.clicked.connect(self.__on_prev_page_clicked)
        return btn

    def __get_next_page_btn(self, context_list: ContextListWidget) -> QPushButton:
        btn = QPushButton(">")
        btn.clicked.connect(self.__on_next_page_clicked)
        btn.setEnabled(context_list.is_word_available())
        return btn

    def __on_prev_page_clicked(self) -> None:
        self._context_list.prev_page()
        self.__update_ui()

    def __on_next_page_clicked(self) -> None:
        self._context_list.next_page()
        self.__update_ui()

    def __close_window(self) -> None:
        self.close()

    def __get_add_to_anki_btn(self) -> QPushButton:
        add_to_anki_btn = QPushButton("Add to anki")
        add_to_anki_btn.clicked.connect(lambda: self.__on_add_to_anki())
        return add_to_anki_btn

    def __get_ignore_btn(self) -> QPushButton:
        res = QPushButton("Ignore")
        res.clicked.connect(lambda: self.__on_ignore())
        return res

    def __get_know_btn(self) -> QPushButton:
        res = QPushButton("I Know It!")
        res.clicked.connect(lambda: self.__on_know())
        return res

    def __get_study_later_btn(self) -> QPushButton:
        res = QPushButton("Study Later")
        res.clicked.connect(lambda: self.__on_study_later())
        return res

    def __on_study_later(self) -> None:
        upsert_word_status(self._context_list.word.text, Status.STUDY_LATER, self.__db)
        self.__update_ui()

    def __on_know(self) -> None:
        upsert_word_status(self._context_list.word.text, Status.KNOWN, self.__db)
        self.__update_ui()

    def __on_ignore(self) -> None:
        upsert_word_status(self._context_list.word.text, Status.IGNORED, self.__db)
        self.__update_ui()

    def __on_add_to_anki(self) -> None:
        mw.onAddCard()
        QApplication.clipboard().setText(self._context_list.word.text)
        tooltip("The word has been copied into the clipboard.", 3000)

        # Set the word status to STUDYING
        upsert_word_status(self._context_list.word.text, Status.STUDYING, self.__db)

        self._context_list.next_page()
        self.__update_ui()

    def __update_ui(self) -> None:
        self._context_list.update_data()
        self._prev_page_btn.setDisabled(self._context_list.get_page_no() == 1)
        self._next_page_btn.setEnabled(self._context_list.is_word_available())
        self._add_to_anki_btn.setDisabled(self.__status == WordStatus.STUDYING)
        self._ignore_btn.setDisabled(self.__status == WordStatus.IGNORED)
        self._know_btn.setDisabled(self.__status == WordStatus.KNOWN)
        self._study_later_btn.setDisabled(self.__status == WordStatus.STUDY_LATER)
