import sys
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QLabel, \
    QMessageBox

from vocab_builder.anki.IAnkiService import IAnkiService
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.document.DocumentWindow import DocumentWindow
from vocab_builder.ui.util.DatabaseUtils import get_prod_vocab_builder_db


class DocumentDetailDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], doc: Document, db: VocabBuilderDB, document_service: DocumentService,
                 anki_service: IAnkiService, show_msg_box: bool = True):
        super(DocumentDetailDialog, self).__init__(parent)
        self.__doc = doc
        self.__db = db
        self.__document_service = document_service
        self.__anki_service = anki_service
        self.__setup_ui(self.__doc, self.__document_service, anki_service, db, show_msg_box)

    def __setup_ui(self, doc: Document, document_service: DocumentService, anki_service: IAnkiService, db: VocabBuilderDB, show_msg_box: bool) -> None:
        vbox = QVBoxLayout()
        self.__add_desc(vbox, doc)
        self.__add_bottom_buttons(vbox, doc, document_service, anki_service, db, show_msg_box)
        self.setLayout(vbox)
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

    def __add_desc(self, vbox: QVBoxLayout, doc: Document) -> None:
        label = QLabel()
        label.setText(doc.name)
        label.setStyleSheet("font-size: 20px;")
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)

    def __add_bottom_buttons(self, vbox: QVBoxLayout, doc: Document, document_service: DocumentService, anki_service: IAnkiService, db: VocabBuilderDB, show_msg_box: bool) -> None:
        hbox = QHBoxLayout()
        self.__add_delete_button(hbox, doc, document_service, show_msg_box)
        self.__add_study_button(hbox, doc, anki_service, db)
        vbox.addLayout(hbox)

    def __add_study_button(self, hbox: QHBoxLayout, doc: Document, anki_service: IAnkiService, db: VocabBuilderDB) -> None:
        self._studyBtn = QPushButton("Study")
        self._studyBtn.setDefault(True)

        self._studyBtn.clicked.connect(lambda: self.__on_study_button_clicked(doc, anki_service, db))

        hbox.addWidget(self._studyBtn)

    def __on_study_button_clicked(self, doc: Document, anki_service: IAnkiService, db: VocabBuilderDB) -> None:
        doc_window = DocumentWindow(doc, db, anki_service)
        doc_window.show()

    def __add_delete_button(self, hbox: QHBoxLayout, doc: Document, document_service: DocumentService, show_msg_box: bool) -> None:
        self._deleteBtn = QPushButton("Delete")
        self._deleteBtn.clicked.connect(lambda: self.__on_delete_button_clicked(doc, document_service, show_msg_box))
        hbox.addWidget(self._deleteBtn)

    def __on_delete_button_clicked(self, doc: Document, document_service: DocumentService, show_msg_box: bool) -> None:
        self._delete_warning_msg_box = QMessageBox()
        self._delete_warning_msg_box.setIcon(QMessageBox.Warning)
        self._delete_warning_msg_box.setText("Are you sure you want to delete this document?")
        self._delete_warning_msg_box.setWindowTitle("Delete")
        self._delete_warning_msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self._delete_warning_msg_box.buttonClicked.connect(lambda btn: self.__delete_dialog_btn_handler(btn, doc, document_service, self._delete_warning_msg_box))
        if show_msg_box:
            self._delete_warning_msg_box.exec_()

    def __delete_dialog_btn_handler(self, button: QMessageBox.StandardButton, doc: Document, document_service: DocumentService, msg_box: QMessageBox) -> None:
        btn_code = msg_box.standardButton(button)
        if btn_code == QMessageBox.Ok:
            # TODO delete the document
            # TODO remove the document in MainDialog
            # TODO test it
            document_service.delete_doc_and_words(doc.document_id)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    doc = Document(1, "test", "test contents")
    db = get_prod_vocab_builder_db()
    document_service = DocumentService(db)
    dialog = DocumentDetailDialog(None, doc, document_service)
    dialog.show()
    sys.exit(app.exec_())