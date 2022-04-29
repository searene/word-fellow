import unittest

import pytest
from PyQt5.QtTest import QTest
from aqt import AnkiApp
from pytestqt.qtbot import QtBot

from anki_testing import anki_running


class DocumentWindowTestCase(unittest.TestCase):

    def test_ignore_and_change_status(self):
        with anki_running() as anki_app:
            print("hello")