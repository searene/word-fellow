from aqt import mw
from aqt.qt import *

from vocab_builder.domain import utils
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.ui.util.DatabaseUtils import prod_vocab_builder_db
from vocab_builder.ui.dialog.MainWindow import MainWindow
import vocab_builder.domain.word.WordService as WordService
import vocab_builder.domain.word.WordValueObject as WordValueObject
from aqt import gui_hooks


def __init_database():
    utils.init_database(prod_vocab_builder_db)
    insert_test_data()


def insert_test_data():
    document_service = DocumentService(prod_vocab_builder_db)
    document_service.remove_all()
    # doc1 = document_service.create_new_document("test name1", "this is this this")
    # doc2 = document_service.create_new_document("test name2", "test_contents2")
    #
    # word_value_objects = [
    #     WordValueObject.WordValueObject("this", doc1.document_id, {"this": [0, 8, 13]}, False),
    #     WordValueObject.WordValueObject("is", doc1.document_id, {"is": [5]}, False)
    # ]
    # WordService.batch_insert(word_value_objects, prod_vocab_builder_db)


def show_main_dialog() -> None:
    main_window = MainWindow(prod_vocab_builder_db)
    main_window.show()


def init_addon() -> None:
    __init_database()
    # create a new menu item, "test"
    action = QAction("Anki Vocab Builder", mw)
    # set it to call testFunction when it's clicked
    qconnect(action.triggered, show_main_dialog)
    # and add it to the tools menu
    mw.form.menuTools.addAction(action)


if __name__ == "__main__":
    init_addon()
