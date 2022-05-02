from typing import TYPE_CHECKING, Callable

from vocab_builder.anki.IAnkiService import IAnkiService
if TYPE_CHECKING:
    from anki.notes import Note


class MockedAnkiService(IAnkiService):

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