from typing import Dict, Optional

from PyQt5.QtWidgets import QWidget

from word_fellow.ui.dialog.document.DocumentDialog import DocumentDialog
from word_fellow.ui.dialog.manager.DialogType import DialogType


class DialogManager:

    _dialogs: Dict[DialogType, (QWidget, Optional[QWidget])] = {
        DialogType.DOCUMENT_DIALOG: (DocumentDialog, None),
    }

    @staticmethod
    def open(dialog_type: DialogType, *args):
        creator, instance = DialogManager._dialogs[dialog_type]
        if instance is not None:
            instance.show()
        else:
            instance = creator(*args)
            instance.show()
            DialogManager._dialogs[dialog_type] = (creator, instance)