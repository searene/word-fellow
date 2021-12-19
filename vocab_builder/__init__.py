from aqt import mw
from aqt.qt import *

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.ui.DatabaseUtils import prod_session
from vocab_builder.ui.MainDialog import MainDialog


def __init_database():
    Document.init_database(prod_session)
    Word.init_database(prod_session)


def show_main_dialog() -> None:
    dialog = MainDialog()
    dialog.show_dialog()


# mw is None when we don't start Anki (e.g. when we are testing)
if mw is not None:
    __init_database()
    # create a new menu item, "test"
    action = QAction("Anki Vocab Builder", mw)
    # set it to call testFunction when it's clicked
    qconnect(action.triggered, show_main_dialog)
    # and add it to the tools menu
    mw.form.menuTools.addAction(action)