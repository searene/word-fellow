from typing import Callable

import aqt

from word_fellow.anki.DefaultAnkiService import DefaultAnkiService
from word_fellow.domain import utils
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from word_fellow.ui.dialog.MainDialog import MainDialog
import word_fellow.domain.word.WordService as WordService
import word_fellow.domain.word.WordValueObject as WordValueObject

from word_fellow.ui.dialog.document.DocumentWindow import DocumentWindow
from word_fellow.ui.util.DatabaseUtils import get_prod_word_fellow_db


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


def show_main_dialog() -> None:
    __init_database()
    db = get_prod_word_fellow_db()
    main_dialog = MainDialog(db, DefaultAnkiService(), DefaultDocumentAnalyzer(db))
    main_dialog.show()
    main_dialog.exec_()


def new_undo(old_undo: Callable[[], None]) -> None:
    active_win = aqt.mw.app.activeWindow()
    if type(active_win) is DocumentWindow:
        active_win.undo()
    else:
        old_undo()


def init_addon() -> None:
    action = aqt.qt.QAction("WordFellow", aqt.mw)
    aqt.qt.qconnect(action.triggered, show_main_dialog)
    aqt.mw.form.menuTools.addAction(action)

    old_undo_func = aqt.mw.undo
    aqt.mw.form.actionUndo.triggered.disconnect()
    aqt.qt.qconnect(aqt.mw.form.actionUndo.triggered, lambda: new_undo(old_undo_func))