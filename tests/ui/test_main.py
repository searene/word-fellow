from anki_testing import anki_running


def test_my_addon():
    with anki_running() as anki_app:
        import ui
        # add some tests in here
        print("test")
