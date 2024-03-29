import os
import sys
from typing import Dict, Optional, TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QFont, QKeySequence
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton, QApplication, QSizePolicy, \
    QSpacerItem, QMenu, QWidget

from ....domain.operation.Operation import Operation

if TYPE_CHECKING:
    from anki.notes import Note

from ....anki.IAnkiService import IAnkiService
from ....anki.MockedAnkiService import MockedAnkiService
from ....domain.backup.BackupService import BackupService
from ....domain.document.Document import Document
from ....domain.document.DocumentService import DocumentService
from ....domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from ....domain.settings.SettingsService import SettingsService
from ....domain.status.GlobalWordStatus import upsert_word_status, Status, delete_word_status, to_status
from ....domain.word.Word import Word
from ....domain.word.WordStatus import WordStatus
from ....infrastructure import WordFellowDB, get_prod_db_path
from ....ui.util.DatabaseUtils import get_test_word_fellow_db
from ....ui.dialog.backup.BackupWindow import BackupWindow
from ....ui.dialog.context.list.ContextListWidget import ContextListWidget
from ....ui.util.PyQtUtils import get_vertical_line


class DocumentWindow(QWidget):

    def __init__(self, doc: Document, db: WordFellowDB, anki_service: IAnkiService):
        super(DocumentWindow, self).__init__()
        self.__status_to_offset_dict: Dict[WordStatus, int] = {}
        self.__anki_service = anki_service
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
        self.__anki_service.add_to_did_add_note_hook(self.__raise)
        self.__operations: [Operation] = []
        self.showMaximized()

    # def reopen(self, parent: Optional[QDialog], doc: Document, db: WordFellowDB, anki_service: IAnkiService):
    #     self.__doc = doc
    #     self.__status_to_offset_dict = {}
    #     self.__operations = []
    #     self.__status = WordStatus.UNREVIEWED
    #     self._status_combo_box.setCurrentText(self.__status.value)
    #     self._context_list.set_status(self.__status)
    #     self.__update_ui()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__anki_service.remove_from_did_add_note_hook(self.__raise)
        event.accept()

    def __show_backup_dialog(self, db: WordFellowDB) -> None:
        settings_service = SettingsService(db)
        backup_service = BackupService(settings_service, db)
        should_run_backup = backup_service.should_backup_today()
        if not should_run_backup:
            return
        self._backup_win = BackupWindow(backup_service)
        self._backup_win.show()

    def __raise(self, note: 'Note'):
        self.raise_()
        self.activateWindow()

    def __get_dialog_layout(self, word_label: QLabel, context_list: ContextListWidget, doc: Document, status: WordStatus, db: WordFellowDB) -> QVBoxLayout:
        vbox = QVBoxLayout()
        vbox.addWidget(word_label)
        vbox.addLayout(self.__get_top_bar())
        vbox.addWidget(context_list)
        vbox.addLayout(self.__get_bottom_bar(doc, status, db))
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

    def __get_page_info_label(self, status: WordStatus, doc: Document, db: WordFellowDB) -> QLabel:
        page_info_label = QLabel()
        page_info_label.setMinimumWidth(50)
        page_info_label.setAlignment(Qt.AlignCenter)
        page_info_label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))
        page_info_label.setToolTip("Current / Total")
        self.__update_page_info_label(page_info_label, status, doc, db)
        return page_info_label

    def __get_total_page_count(self, status: WordStatus, doc: Document, db: WordFellowDB) -> int:
        return doc.get_word_count(status, db)

    def __get_status_combo_box(self) -> QComboBox:
        status_combo_box = QComboBox()
        for status in WordStatus:
            status_combo_box.addItem(status.value)
        status_combo_box.currentTextChanged.connect(self.__on_status_selected)
        return status_combo_box

    def __on_status_selected(self, status_value: str) -> None:
        self.__operations = []
        self.__status = WordStatus(status_value)
        self._context_list.set_status(self.__status)
        self.__update_ui()

    def __get_context_list(self, word: Optional[Word], doc: Document, status: WordStatus, db: WordFellowDB, status_to_offset_dict: Dict[WordStatus, int]) -> ContextListWidget:
        context_list = ContextListWidget(self, word, doc, status, db, status_to_offset_dict)
        return context_list

    def __get_middle_area(self, context_list: ContextListWidget) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(context_list)
        return hbox

    def __get_bottom_bar(self, doc: Document, status: WordStatus, db: WordFellowDB) -> QHBoxLayout:
        res = QHBoxLayout()

        self._add_to_anki_btn = self.__get_add_to_anki_btn(self.__is_word_available())
        self._ignore_btn = self.__get_ignore_btn(self.__is_word_available())
        self._know_btn = self.__get_know_btn(self.__is_word_available())
        self._study_later_btn = self.__get_study_later_btn(self.__is_word_available())
        res.addWidget(self._add_to_anki_btn)
        res.addWidget(self._ignore_btn)
        res.addWidget(self._know_btn)
        res.addWidget(self._study_later_btn)
        res.addWidget(get_vertical_line())
        res.addWidget(self.__get_more_btn())
        res.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self._prev_page_btn = self.__get_prev_page_btn()
        self._page_info_label = self.__get_page_info_label(status, doc, db)
        self._next_page_btn = self.__get_next_page_btn()
        res.addWidget(self._prev_page_btn)
        res.addWidget(self._page_info_label)
        res.addWidget(self._next_page_btn)

        return res

    def __get_prev_page_btn(self) -> QPushButton:
        btn = QPushButton("<")
        btn.setDisabled(True)
        btn.setShortcut("Left")
        btn.clicked.connect(self.__prev_page)
        btn.setToolTip("Previous word")
        return btn

    def __get_next_page_btn(self) -> QPushButton:
        btn = QPushButton(">")
        btn.clicked.connect(self.__next_page)
        btn.setShortcut("Right")
        btn.setEnabled(self.__is_word_available())
        btn.setToolTip("Next word")
        return btn

    def __close_window(self) -> None:
        self.close()

    def __get_add_to_anki_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("Add to anki (a)")
        res.setEnabled(is_word_available)
        res.setShortcut("a")
        res.setToolTip("Add the word to your anki deck")
        res.clicked.connect(lambda: self.__on_add_to_anki())
        return res

    def __get_ignore_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("Ignore (i)")
        res.setShortcut("i")
        res.setEnabled(is_word_available)
        res.clicked.connect(lambda: self.__on_ignore())
        res.setToolTip("Ignore the word. You don't need to learn it.")
        return res

    def __get_know_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("I Know It (k)")
        res.setShortcut("k")
        res.setEnabled(is_word_available)
        res.clicked.connect(lambda: self.__on_know())
        res.setToolTip("Click it if you know the word, thus you don't need to add it to Anki.")
        return res

    def __get_study_later_btn(self, is_word_available: bool) -> QPushButton:
        res = QPushButton("Study Later (s)")
        res.setShortcut("s")
        res.setEnabled(is_word_available)
        res.clicked.connect(lambda: self.__on_study_later())
        res.setToolTip("Click it if you don't know the word, and you don't want to add it to anki now, you want to do it later.")
        return res

    def __on_study_later(self) -> None:
        self.__operations.append(Operation(self.__word.text, self.__status, WordStatus.STUDY_LATER))
        upsert_word_status(self.__word.text, Status.STUDY_LATER, self.__db)
        self.__adjust_page_no(self.__status_to_offset_dict, self.__status, self.__total_page)
        self.__update_ui()

    def __on_know(self) -> None:
        self.__operations.append(Operation(self.__word.text, self.__status, WordStatus.KNOWN))
        upsert_word_status(self.__word.text, Status.KNOWN, self.__db)
        self.__adjust_page_no(self.__status_to_offset_dict, self.__status, self.__total_page)
        self.__update_ui()

    def __on_ignore(self) -> None:
        self.__operations.append(Operation(self.__word.text, self.__status, WordStatus.IGNORED))
        upsert_word_status(self.__word.text, Status.IGNORED, self.__db)
        self.__adjust_page_no(self.__status_to_offset_dict, self.__status, self.__total_page)
        self.__update_ui()

    def __on_add_to_anki(self) -> None:
        self.__operations.append(Operation(self.__word.text, self.__status, WordStatus.STUDYING))
        QApplication.clipboard().setText(self.__word.text)
        self.__anki_service.show_tooltip("The word has been copied into the clipboard")

        # Set the word status to STUDYING
        upsert_word_status(self.__word.text, Status.STUDYING, self.__db)

        self.__adjust_page_no(self.__status_to_offset_dict, self.__status, self.__total_page)
        self.__update_ui()
        self.__anki_service.show_add_card_dialog()

    def __at_last_page(self, current_page: int, total_page: int) -> bool:
        return current_page == total_page

    def __adjust_page_no(self, status_to_offset_dict: Dict[WordStatus, int], status: WordStatus, total_page: int) -> None:
        current_page = status_to_offset_dict[status] + 1
        if self.__at_last_page(current_page, total_page) and current_page > 1:
            status_to_offset_dict[status] -= 1

    def __update_ui(self) -> None:
        self.__word = self.__get_word(self.__doc, self.__status, self.__status_to_offset_dict, self.__db)
        self._word_label.setText(self.__get_word_label_text(self.__word))
        self._context_list.set_word(self.__word)
        self._context_list.update_data()
        self._prev_page_btn.setDisabled(self.__get_page_no() == 1)
        self._next_page_btn.setEnabled(self.__get_page_no() < self.__get_total_page_count(self.__status, self.__doc, self.__db))
        self._add_to_anki_btn.setDisabled(self.__status == WordStatus.STUDYING or (not self.__is_word_available()))
        self._ignore_btn.setDisabled(self.__status == WordStatus.IGNORED or (not self.__is_word_available()))
        self._know_btn.setDisabled(self.__status == WordStatus.KNOWN or (not self.__is_word_available()))
        self._study_later_btn.setDisabled(self.__status == WordStatus.STUDY_LATER or (not self.__is_word_available()))
        self.__update_page_info_label(self._page_info_label, self.__status, self.__doc, self.__db)

    def __update_page_info_label(self, page_info_label: QLabel, status: WordStatus, doc: Document, db: WordFellowDB) -> None:
        if self.__is_word_available():
            current_page = self.__get_page_no()
            self.__total_page = self.__get_total_page_count(status, doc, db)
            page_info_label.setText(f"{current_page} / {self.__total_page}")
        else:
            page_info_label.setText("- / -")

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
                   db: WordFellowDB) -> Optional[Word]:
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
        res.setFixedHeight(100)
        res.setText(self.__get_word_label_text(word))
        res.setStyleSheet("QLabel { border: 1px solid #B7B7B7; }")
        return res

    def __get_word_label_text(self, word: Optional[Word]) -> str:
        return word.text if word is not None else "--"

    def __get_more_btn(self) -> QPushButton:
        more_btn = QPushButton(self)
        more_btn.setText("More")

        menu = QMenu(self)
        self._undo_action = menu.addAction("Undo")
        self._undo_action.triggered.connect(lambda action: self.undo())
        self._undo_action.setShortcut(QKeySequence.Undo)
        more_btn.setMenu(menu)
        return more_btn

    def undo(self):
        if len(self.__operations) == 0:
            return
        last_op: Operation = self.__operations.pop()
        if last_op.prev_status == WordStatus.UNREVIEWED:
            delete_word_status(last_op.word, to_status(word_status=last_op.next_status), self.__db)
        else:
            upsert_word_status(last_op.word, to_status(word_status=last_op.prev_status), self.__db)
        self.__update_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()
    analyzer = DefaultDocumentAnalyzer(db)
    document_service = DocumentService(db)
    doc = document_service.import_document("test_name", "test contents", analyzer)
    doc_window = DocumentWindow(doc, db, MockedAnkiService(app))
    doc_window.show()
    app.exec_()
    db.destroy()