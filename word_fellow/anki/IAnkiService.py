from typing import Protocol, Callable, TYPE_CHECKING, Optional
from abc import abstractmethod

from PyQt5.QtWidgets import QApplication

if TYPE_CHECKING:
    from anki.notes import Note


class IAnkiService(Protocol):

    @abstractmethod
    def show_add_card_dialog(self) -> None:
        pass

    @abstractmethod
    def show_tooltip(self, tooltip: str) -> None:
        pass

    @abstractmethod
    def add_to_did_add_note_hook(self, callback: Callable[['Note'], None]) -> None:
        pass

    @abstractmethod
    def remove_from_did_add_note_hook(self, callback: Callable[['Note'], None]) -> None:
        pass

    @abstractmethod
    def show_info_dialog(self, info: str) -> None:
        pass

    @abstractmethod
    def get_app(self) -> QApplication:
        pass
