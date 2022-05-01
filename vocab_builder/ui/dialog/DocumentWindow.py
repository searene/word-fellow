from typing import Callable, Dict, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QApplication, QWidget, \
    QSizePolicy, QSpacerItem
from anki.notes import Note

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.status.GlobalWordStatus import upsert_word_status, Status
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.context.list.ContextListWidget import ContextListWidget
import aqt


class DocumentWindow(QWidget):

    def __init__(self, doc: Document, db: VocabBuilderDB, anki_add_card_handler: Callable[[], None]):
        super(DocumentWindow, self).__init__()
        self.__anki_add_card_handler = anki_add_card_handler
        self.__status_to_offset_dict: Dict[WordStatus, int] = {}
        self.__db = db
        self.__doc = doc
        self.__offset = 0
        self._status_combo_box = self.__get_status_combo_box()
        self.__status = WordStatus(self._status_combo_box.currentText())
        self.__word = self.__get_word(doc, self.__status, self.__status_to_offset_dict, db)
        self._word_label = self.__get_word_label(self.__word)
        self._context_list = self.__get_context_list(self.__word, self.__doc, self.__status, db, self.__status_to_offset_dict)
        self.__dialog_layout = self.__get_dialog_layout(self._word_label, self._context_list, doc, self.__status, self.__db)
        self.__init_ui(self.__dialog_layout)
        aqt.gui_hooks.add_cards_did_add_note.append(self.__raise)
        self.showMaximized()

    def closeEvent(self, event: QCloseEvent) -> None:
        aqt.gui_hooks.add_cards_did_add_note.remove(self.__raise)

    def __raise(self, note: Note):
        self.raise_()

    def __get_dialog_layout(self, word_label: QLabel, context_list: ContextListWidget, doc: Document, status: WordStatus, db: VocabBuilderDB) -> QVBoxLayout:
        vbox = QVBoxLayout()
        vbox.addWidget(word_label)
        vbox.addLayout(self.__get_top_bar())
        vbox.addWidget(context_list)
        vbox.addLayout(self.__get_bottom_bar(context_list, doc, status, db))
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

    def __get_page_info_label(self, status: WordStatus, doc: Document, db: VocabBuilderDB, context_list: ContextListWidget) -> QLabel:
        page_info_label = QLabel()
        page_info_label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))
        page_info_label.setToolTip("Current / Total")
        self.__update_page_info_label(page_info_label, status, doc, db)
        return page_info_label

    def __get_total_page_count(self, status: WordStatus, doc: Document, db: VocabBuilderDB) -> int:
        return doc.get_word_count(status, db)

    def __get_status_combo_box(self) -> QComboBox:
        status_combo_box = QComboBox()
        for status in WordStatus:
            status_combo_box.addItem(status.value)
        status_combo_box.currentTextChanged.connect(self.__on_status_selected)
        return status_combo_box

    def __on_status_selected(self, status_value: str) -> None:
        self.__status = WordStatus(status_value)
        self._context_list.set_status(self.__status)
        self.__update_ui()

    def __get_context_list(self, word: Optional[Word], doc: Document, status: WordStatus, db: VocabBuilderDB, status_to_offset_dict: Dict[WordStatus, int]) -> ContextListWidget:
        context_list = ContextListWidget(word, doc, status, db, status_to_offset_dict)
        return context_list

    def __get_middle_area(self, context_list: ContextListWidget) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(context_list)
        return hbox

    def __get_bottom_bar(self, context_list: ContextListWidget, doc: Document, status: WordStatus, db: VocabBuilderDB) -> QHBoxLayout:
        res = QHBoxLayout()

        self._add_to_anki_btn = self.__get_add_to_anki_btn(self.__is_word_available())
        self._ignore_btn = self.__get_ignore_btn(self.__is_word_available())
        self._know_btn = self.__get_know_btn(self.__is_word_available())
        self._study_later_btn = self.__get_study_later_btn(self.__is_word_available())
        res.addWidget(self._add_to_anki_btn)
        res.addWidget(self._ignore_btn)
        res.addWidget(self._know_btn)
        res.addWidget(self._study_later_btn)
        res.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self._prev_page_btn = self.__get_prev_page_btn()
        self._page_info_label = self.__get_page_info_label(status, doc, db, context_list)
        self._next_page_btn = self.__get_next_page_btn(context_list)
        res.addWidget(self._prev_page_btn)
        res.addWidget(self._page_info_label)
        res.addWidget(self._next_page_btn)

        return res

    def __get_prev_page_btn(self) -> QPushButton:
        btn = QPushButton("<")
        btn.setDisabled(True)
        btn.clicked.connect(self.__prev_page)
        btn.setToolTip("Previous word")
        return btn

    def __get_next_page_btn(self, context_list: ContextListWidget) -> QPushButton:
        btn = QPushButton(">")
        btn.clicked.connect(self.__next_page)
        btn.setEnabled(self.__is_word_available())
        btn.setToolTip("Next word")
        return btn

    def __close_window(self) -> None:
        self.close()

    def __get_add_to_anki_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("Add to anki")
        res.setEnabled(is_word_available)
        res.clicked.connect(lambda: self.__on_add_to_anki())
        res.setToolTip("Add the word to your anki deck")
        return res

    def __get_ignore_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("Ignore")
        res.setEnabled(is_word_available)
        res.clicked.connect(lambda: self.__on_ignore())
        res.setToolTip("Ignore the word. You don't need to learn it.")
        return res

    def __get_know_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("I Know It")
        res.setEnabled(is_word_available)
        res.clicked.connect(lambda: self.__on_know())
        res.setToolTip("Click it if you know the word, thus you don't need to add it to Anki.")
        return res

    def __get_study_later_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("Study Later")
        res.setEnabled(is_word_available)
        res.clicked.connect(lambda: self.__on_study_later())
        res.setToolTip("Click it if you don't know the word, and you don't want to add it to anki now, you want to do it later.")
        return res

    def __on_study_later(self) -> None:
        upsert_word_status(self.__word.text, Status.STUDY_LATER, self.__db)
        self.__update_ui()

    def __on_know(self) -> None:
        upsert_word_status(self.__word.text, Status.KNOWN, self.__db)
        self.__update_ui()

    def __on_ignore(self) -> None:
        upsert_word_status(self.__word.text, Status.IGNORED, self.__db)
        self.__update_ui()

    def __on_add_to_anki(self) -> None:
        self.__anki_add_card_handler()
        QApplication.clipboard().setText(self.__word.text)
        aqt.utils.tooltip("The word has been copied into the clipboard.", 3000)

        # Set the word status to STUDYING
        upsert_word_status(self.__word.text, Status.STUDYING, self.__db)

        self.__update_ui()

    def __update_ui(self) -> None:
        # TODO Go to previous page if pageNo > 1 and we have no word in the current page
        self.__word = self.__get_word(self.__doc, self.__status, self.__status_to_offset_dict, self.__db)
        self._word_label.setText(self.__get_word_label_text(self.__word))
        self._context_list.set_word(self.__word)
        self._context_list.update_data()
        self._prev_page_btn.setDisabled(self.__get_page_no() == 1)
        # TODO Just disable the next page button when we are at the last page.
        self._next_page_btn.setEnabled(self.__is_word_available())
        self._add_to_anki_btn.setDisabled(self.__status == WordStatus.STUDYING or (not self.__is_word_available()))
        self._ignore_btn.setDisabled(self.__status == WordStatus.IGNORED or (not self.__is_word_available()))
        self._know_btn.setDisabled(self.__status == WordStatus.KNOWN or (not self.__is_word_available()))
        self._study_later_btn.setDisabled(self.__status == WordStatus.STUDY_LATER or (not self.__is_word_available()))
        self.__update_page_info_label(self._page_info_label, self.__status, self.__doc, self.__db)

    def __update_page_info_label(self, page_info_label: QLabel, status: WordStatus, doc: Document, db: VocabBuilderDB) -> None:
        if self.__is_word_available():
            self.__current_page_no = self.__get_page_no()
            self.__total_page_count = self.__get_total_page_count(status, doc, db)
            page_info_label.setText(f"{self.__current_page_no} / {self.__total_page_count}")
        else:
            self.__current_page_no = None
            self.__total_page_count = None
            page_info_label.setText("")

    def __get_page_no(self) -> int:
        """Get the page number of the current status, starting with 1."""
        return self.__status_to_offset_dict[self.__status] + 1

    def __prev_page(self):
        self.__status_to_offset_dict[self.__status] = self.__status_to_offset_dict[self.__status] - 1
        self.__update_ui()

    def __next_page(self):
        self.__status_to_offset_dict[self.__status] = self.__status_to_offset_dict[self.__status] + 1
        self.__update_ui()

    def __get_word(self, doc: Document, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int],
                   db: VocabBuilderDB) -> Optional[Word]:
        offset = self.__get_offset(status, status_to_offset_dict)
        return doc.get_next_word(offset, status, db)

    def __get_offset(self, status: WordStatus, status_to_offset_dict: Dict[WordStatus, int]) -> int:
        if status not in status_to_offset_dict:
            status_to_offset_dict[status] = 0
        return status_to_offset_dict[status]
    
    def __is_word_available(self) -> bool:
        return self.__word is not None

    def __get_word_label(self, word: Optional[Word]) -> QLabel:
        res = QLabel(self)
        font = QFont()
        font.setPointSize(24)
        res.setFont(font)
        res.setAlignment(Qt.AlignCenter)
        res.setMargin(20)
        res.setText(self.__get_word_label_text(word))
        return res

    def __get_word_label_text(self, word: Optional[Word]) -> str:
        return word.text if word is not None else "--"

