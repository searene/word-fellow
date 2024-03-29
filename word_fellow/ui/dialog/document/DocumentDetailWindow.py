import os
import sys
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QLabel, \
    QMessageBox

from ....anki.IAnkiService import IAnkiService
from ....anki.MockedAnkiService import MockedAnkiService
from ....domain.document.Document import Document
from ....domain.document.DocumentService import DocumentService
from ....infrastructure import WordFellowDB
from ....ui.util.DatabaseUtils import get_test_word_fellow_db
from ....ui.dialog.document.DocumentWindow import DocumentWindow


class DocumentDetailWindow(QWidget):

    def __init__(self, doc: Document, db: WordFellowDB, document_service: DocumentService,
                 anki_service: IAnkiService, on_document_removed: Callable[[], None], show_dialog: bool = True):
        super(DocumentDetailWindow, self).__init__()
        self.__doc = doc
        self.__db = db
        self.__document_service = document_service
        self.__anki_service = anki_service
        self.__setup_ui(self.__doc, self.__document_service, anki_service, db, on_document_removed, show_dialog)

    def __setup_ui(self, doc: Document, document_service: DocumentService, anki_service: IAnkiService, db: WordFellowDB,
                   on_document_removed: Callable[[], None], show_dialog: bool) -> None:
        vbox = QVBoxLayout()
        self.__add_desc(vbox, doc)
        self.__add_bottom_buttons(vbox, doc, document_service, anki_service, db, on_document_removed, show_dialog)
        self.setLayout(vbox)
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

    def __add_desc(self, vbox: QVBoxLayout, doc: Document) -> None:
        label = QLabel()
        label.setText(doc.name)
        label.setStyleSheet("font-size: 20px;")
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)

    def __add_bottom_buttons(self, vbox: QVBoxLayout, doc: Document, document_service: DocumentService,
                             anki_service: IAnkiService, db: WordFellowDB, on_document_removed: Callable[[], None],
                             show_dialog: bool) -> None:
        hbox = QHBoxLayout()
        self.__add_delete_button(hbox, doc, document_service, on_document_removed, show_dialog)
        self.__add_study_button(hbox, doc, anki_service, db)
        vbox.addLayout(hbox)

    def __add_study_button(self, hbox: QHBoxLayout, doc: Document, anki_service: IAnkiService, db: WordFellowDB) -> None:
        self._studyBtn = QPushButton("Study")
        self._studyBtn.setDefault(True)

        self._studyBtn.clicked.connect(lambda: self.__on_study_button_clicked(doc, anki_service, db))

        hbox.addWidget(self._studyBtn)

    def __on_study_button_clicked(self, doc: Document, anki_service: IAnkiService, db: WordFellowDB) -> None:
        self._doc_window = DocumentWindow(doc, db, anki_service)
        self._doc_window.show()
        self.close()

    def __add_delete_button(self, hbox: QHBoxLayout, doc: Document, document_service: DocumentService,
                            on_document_removed: Callable[[], None], show_dialog: bool) -> None:
        self._delete_btn = QPushButton("Delete")
        self._delete_btn.clicked.connect(lambda: self.__on_delete_button_clicked(doc, document_service, on_document_removed, show_dialog))
        hbox.addWidget(self._delete_btn)

    def __on_delete_button_clicked(self, doc: Document, document_service: DocumentService,
                                   on_document_removed: Callable[[], None], show_dialog: bool) -> None:
        self._delete_warning_msg_box = QMessageBox(self)
        self._delete_warning_msg_box.setIcon(QMessageBox.Warning)
        self._delete_warning_msg_box.setText("Are you sure you want to delete this document?\n\nMarked words (such as known, added to anki, study later, ignored) won't be deleted")
        self._delete_warning_msg_box.setWindowTitle("Delete")
        self._delete_warning_msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self._delete_warning_msg_box.buttonClicked.connect(lambda btn: self.__delete_dialog_btn_handler(btn, doc, document_service, self._delete_warning_msg_box))
        if show_dialog:
            self._delete_warning_msg_box.exec()
        on_document_removed()

    def __delete_dialog_btn_handler(self, button: QMessageBox.StandardButton, doc: Document, document_service: DocumentService, msg_box: QMessageBox) -> None:
        btn_code = msg_box.standardButton(button)
        if btn_code == QMessageBox.Ok:
            document_service.delete_doc_and_words(doc.document_id)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    doc = Document(1, "test", "test contents")
    db = get_test_word_fellow_db()
    document_service = DocumentService(db)
    detail_window = DocumentDetailWindow(doc, db, document_service, MockedAnkiService(app),
                                         on_document_removed=lambda: None, show_dialog=True)
    detail_window.show()
    code = app.exec_()
    db.destroy()
    sys.exit(code)