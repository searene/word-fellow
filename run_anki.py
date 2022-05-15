from aqt import _run
from word_fellow.ui import init_addon

# Initialize Anki
app = _run(exec=False)

# Initialize our addon
init_addon()

# Run anki
app.exec()
