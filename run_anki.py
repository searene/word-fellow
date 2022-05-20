from tests.anki_testing import anki_running
from word_fellow.ui import init_addon

with anki_running() as app:
    # Initialize our addon
    init_addon()

    # Run anki
    app.exec()
