from aqt import _run

# Initialize Anki
app = _run(exec=False)

# Initialize our addon
from vocab_builder.ui import init_addon
init_addon()

# Run anki
app.exec()
