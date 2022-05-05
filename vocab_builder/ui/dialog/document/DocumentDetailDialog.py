import sys
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QPushButton, QApplication, QLabel

from vocab_builder.anki.IAnkiService import IAnkiService
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.ui.util.DatabaseUtils import get_prod_vocab_builder_db


class DocumentDetailDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], doc: Document, document_service: DocumentService, anki_service: IAnkiService):
        super(DocumentDetailDialog, self).__init__(parent)
        self.__doc = doc
        self.__document_service = document_service
        self.__anki_service = anki_service
        self.__setup_ui(self.__doc, self.__document_service)

    def __setup_ui(self, doc: Document, document_service: DocumentService) -> None:
        vbox = QVBoxLayout()
        self.__add_desc(vbox, doc)
        self.__add_bottom_buttons(vbox, doc, document_service)
        self.setLayout(vbox)
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

    def __add_desc(self, vbox: QVBoxLayout, doc: Document) -> None:
        label = QLabel()
        label.setText(doc.name)
        label.setStyleSheet("font-size: 20px;")
        label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label)

    def __add_bottom_buttons(self, vbox: QVBoxLayout, doc: Document, document_service: DocumentService) -> None:
        hbox = QHBoxLayout()
        self.__add_delete_button(hbox, doc, document_service)
        self.__add_study_button(hbox, doc, document_service)
        vbox.addLayout(hbox)

    def __add_study_button(self, hbox: QHBoxLayout, doc: Document, document_service: DocumentService) -> None:
        self._studyBtn = QPushButton("Study")
        self._studyBtn.setDefault(True)
        hbox.addWidget(self._studyBtn)

    def __add_delete_button(self, hbox: QHBoxLayout, doc: Document, document_service: DocumentService) -> None:
        self._deleteBtn = QPushButton("Delete")
        p = self._deleteBtn.palette()
        p.setColor(self._deleteBtn.backgroundRole(), Qt.red)
        self._deleteBtn.setPalette(p)
        hbox.addWidget(self._deleteBtn)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    doc = Document(1, "test", "test contents")
    db = get_prod_vocab_builder_db()
    document_service = DocumentService(db)
    dialog = DocumentDetailDialog(None, doc, document_service)
    dialog.show()
    sys.exit(app.exec_())