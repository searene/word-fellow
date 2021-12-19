from PyQt5.QtWidgets import QFrame


def get_horizontal_line() -> QFrame:
    result = QFrame()
    result.setFrameShape(QFrame.HLine)
    result.setFrameShadow(QFrame.Sunken)
    return result
