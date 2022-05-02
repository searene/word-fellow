from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QHBoxLayout, QPushButton

from vocab_builder.ui.dialog.context.list.ClickableListWidget import ClickableListWidget


class BackupTab(QWidget):
    def __init__(self, parent=None):
        super(BackupTab, self).__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        vbox = QVBoxLayout()
        # self.setStyleSheet("QLabel { margin-top: 10; } * {border: 1px solid black; }")
        self.__add_enable_backup_checkbox(vbox)
        self.__add_backup_count(vbox)
        self.__add_backup_path(vbox)
        self.__add_backup_list(vbox)
        self.setLayout(vbox)

    def __add_enable_backup_checkbox(self, vbox: QVBoxLayout) -> None:
        self._enable_backup_checkbox = QCheckBox("Enable Backup")
        vbox.addWidget(self._enable_backup_checkbox)

    def __add_backup_count(self, vbox: QVBoxLayout) -> None:
        backup_count_label = QLabel("Backup Count")
        self._backup_count_line_edit = QLineEdit()
        vbox.addWidget(backup_count_label)
        vbox.addWidget(self._backup_count_line_edit)

    def __add_backup_path(self, vbox: QVBoxLayout) -> None:

        back_path_vbox = QVBoxLayout()
        back_path_vbox.setContentsMargins(0, 0, 0, 0)
        backup_path_label = QLabel("Backup Path")
        back_path_vbox.addWidget(backup_path_label)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self._back_path_line_edit = QLineEdit()
        self._back_path_change_btn = QPushButton("Change")
        hbox.addWidget(self._back_path_line_edit)
        hbox.addWidget(self._back_path_change_btn)
        back_path_vbox.addLayout(hbox)

        vbox.addLayout(back_path_vbox)

    def __add_backup_list(self, vbox: QVBoxLayout) -> None:
        backup_list_label = QLabel("Backup List")
        self._back_list_widget = ClickableListWidget()
        vbox.addWidget(backup_list_label)
        vbox.addWidget(self._back_list_widget)