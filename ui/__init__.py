from aqt import mw
from aqt.qt import *
from ui.main_dialog import MainDialog


def testFunction() -> None:
    example = MainDialog()
    example.show_dialog()


# create a new menu item, "test"
action = QAction("Anki Vocab Builder", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
