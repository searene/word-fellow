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
    # insert_test_data()


def insert_test_data():
    db = get_prod_word_fellow_db()
    db.execute("delete from documents")
    db.execute("delete from words")
    db.execute("delete from global_word_status")
    document_service = DocumentService(get_prod_word_fellow_db())
    doc1 = document_service.create_new_document("test name1", "this is this this")
    doc2 = document_service.create_new_document("test name2", "skip\nto skip\nthis")

    word_value_objects = [
        WordValueObject.WordValueObject("this", doc1.document_id, {"this": [0, 8, 13]}),
        WordValueObject.WordValueObject("is", doc1.document_id, {"is": [5]})
    ]
    WordService.batch_insert(word_value_objects, get_prod_word_fellow_db())


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