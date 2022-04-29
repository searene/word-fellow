from aqt import _run
from vocab_builder.ui import init_addon

# Initialize Anki

app = _run(exec=False)

# Initialize our addon
init_addon()

# Run anki
app.exec()
