import sys

import aqt

from word_fellow.ui import init_addon


if 'unittest' not in sys.modules.keys() and aqt.mw is not None:
    # Only initialize the addon when the addon is not being tested and Anki is running
    init_addon()
