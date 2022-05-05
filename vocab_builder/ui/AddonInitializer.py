import aqt

from vocab_builder.anki.DefaultAnkiService import DefaultAnkiService
from vocab_builder.domain import utils
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.ui.dialog.MainDialog import MainDialog
import vocab_builder.domain.word.WordService as WordService
import vocab_builder.domain.word.WordValueObject as WordValueObject

from vocab_builder.ui.util.DatabaseUtils import get_prod_vocab_builder_db


def __init_database():
    utils.init_database(get_prod_vocab_builder_db())
    # insert_test_data()


def insert_test_data():
    db = get_prod_vocab_builder_db()
    db.execute("delete from documents")
    db.execute("delete from words")
    db.execute("delete from global_word_status")
    document_service = DocumentService(get_prod_vocab_builder_db())
    doc1 = document_service.create_new_document("test name1", "this is this this")
    doc2 = document_service.create_new_document("test name2", "skip\nto skip\nthis")

    word_value_objects = [
        WordValueObject.WordValueObject("this", doc1.document_id, {"this": [0, 8, 13]}),
        WordValueObject.WordValueObject("is", doc1.document_id, {"is": [5]})
    ]
    WordService.batch_insert(word_value_objects, get_prod_vocab_builder_db())


def show_main_dialog() -> None:
    __init_database()
    db = get_prod_vocab_builder_db()
    main_dialog = MainDialog(db, DefaultAnkiService())
    main_dialog.show()
    main_dialog.exec_()


def init_addon() -> None:
    action = aqt.qt.QAction("Anki Vocab Builder", aqt.mw)
    aqt.qt.qconnect(action.triggered, show_main_dialog)
    aqt.mw.form.menuTools.addAction(action)
