import unittest

from anki_testing import anki_running


class UiTestCase(unittest.TestCase):

    def test_my_addon(self):
        with anki_running() as anki_app:
            # add some tests in here
            print("test")
