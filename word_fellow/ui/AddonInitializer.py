from typing import Callable, Optional

import aqt

from ..anki.DefaultAnkiService import DefaultAnkiService
from ..domain import utils
from ..domain.document.DocumentService import DocumentService
from ..domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from ..ui.dialog.DocumentListWindow import DocumentListWindow
from ..ui.dialog.document.DocumentWindow import DocumentWindow
from ..ui.util.DatabaseUtils import get_prod_word_fellow_db
from ..domain.word import WordService
from ..domain.word import WordValueObject


document_list_window: Optional[DocumentListWindow] = None


def __init_database():
    utils.init_database(get_prod_word_fellow_db())


def show_doc_list_window() -> None:
    __init_database()
    db = get_prod_word_fellow_db()
    document_list_window = DocumentListWindow(db, DefaultAnkiService(), DefaultDocumentAnalyzer(db))
    document_list_window.show()


def new_undo(old_undo: Callable[[], None]) -> None:
    active_win = aqt.mw.app.activeWindow()
    if type(active_win) is DocumentWindow:
        active_win.undo()
    else:
        old_undo()


def init_addon() -> None:
    action = aqt.qt.QAction("WordFellow", aqt.mw)
    aqt.qt.qconnect(action.triggered, show_doc_list_window)
    aqt.mw.form.menuTools.addAction(action)

    old_undo_func = aqt.mw.undo
    aqt.mw.form.actionUndo.triggered.disconnect()
    aqt.qt.qconnect(aqt.mw.form.actionUndo.triggered, lambda: new_undo(old_undo_func))