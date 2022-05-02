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
    insert_test_data()


def insert_test_data():
    document_service = DocumentService(get_prod_vocab_builder_db())
    document_service.remove_all()
    doc1 = document_service.create_new_document("test name1", "this is this this")
    doc2 = document_service.create_new_document("test name2", "test_contents2")

    word_value_objects = [
        WordValueObject.WordValueObject("this", doc1.document_id, {"this": [0, 8, 13]}),
        WordValueObject.WordValueObject("is", doc1.document_id, {"is": [5]})
    ]
    WordService.batch_insert(word_value_objects, get_prod_vocab_builder_db())


def show_main_dialog() -> None:
    main_dialog = MainDialog(get_prod_vocab_builder_db(), DefaultAnkiService())
    main_dialog.show()
    main_dialog.exec_()


def init_addon() -> None:
    __init_database()
    # create a new menu item, "test"
    action = aqt.qt.QAction("Anki Vocab Builder", aqt.mw)
    # set it to call testFunction when it's clicked
    aqt.qt.qconnect(action.triggered, show_main_dialog)
    # and add it to the tools menu
    aqt.mw.form.menuTools.addAction(action)
