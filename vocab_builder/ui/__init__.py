from aqt import mw
from aqt.qt import *

from vocab_builder.domain import utils
from vocab_builder.domain.document.DocumentFactory import DocumentFactory
from vocab_builder.ui.DatabaseUtils import prod_session
from vocab_builder.ui.DatabaseUtils import prod_vocab_builder_db
from vocab_builder.ui.MainDialog import MainDialog


def __init_database():
    utils.init_database(prod_session)
    insert_test_data()


def insert_test_data():
    document_factory = DocumentFactory(prod_session)
    document_factory.create_new_document("test name1", "test_contents1")
    document_factory.create_new_document("test name2", "test_contents2")


def show_main_dialog() -> None:
    dialog = MainDialog()
    dialog.show_dialog()


__init_database()
# create a new menu item, "test"
action = QAction("Anki Vocab Builder", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, show_main_dialog)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
