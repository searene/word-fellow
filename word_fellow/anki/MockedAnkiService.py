from typing import TYPE_CHECKING, Callable, Optional

from PyQt5.QtWidgets import QApplication

from word_fellow.anki.IAnkiService import IAnkiService

if TYPE_CHECKING:
    from anki.notes import Note


class MockedAnkiService(IAnkiService):

    def __init__(self, app: QApplication):
        self.__app = app

    def show_add_card_dialog(self) -> None:
        pass

    def show_tooltip(self, tooltip: str) -> None:
        pass

    def add_to_did_add_note_hook(self, callback: Callable[['Note'], None]) -> None:
        pass

    def remove_from_did_add_note_hook(self, callback: Callable[['Note'], None]) -> None:
        pass

    def show_info_dialog(self, info: str) -> None:
        pass

    def get_app(self) -> QApplication:
        return self.__app
