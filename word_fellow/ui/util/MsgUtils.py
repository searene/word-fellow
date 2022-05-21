from PyQt5.QtWidgets import QMessageBox, QWidget


def show_warning_with_ok_btn(parent: QWidget, title: str, msg: str, show_ui: bool) -> QMessageBox:
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Warning)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    if show_ui:
        msg_box.exec()
    return msg_box


def show_info_with_ok_btn(parent: QWidget, title: str, msg: str, show_ui: bool) -> QMessageBox:
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(msg)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    if show_ui:
        msg_box.exec_()
    return msg_box
