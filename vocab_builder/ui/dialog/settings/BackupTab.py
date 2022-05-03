import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, \
    QApplication

from tests.utils import get_test_vocab_builder_db
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.context.list.ClickableListWidget import ClickableListWidget


class BackupTab(QWidget):
    def __init__(self, db: VocabBuilderDB):
        super(BackupTab, self).__init__()
        self.__db = db
        self.__setup_ui()

    def __setup_ui(self) -> None:
        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        self.__add_enable_backup_checkbox(vbox)
        self.__add_backup_count(vbox)
        self.__add_backup_path(vbox)
        self.__add_backup_list(vbox)
        self.setLayout(vbox)

    def __add_enable_backup_checkbox(self, vbox: QVBoxLayout) -> None:
        self._enable_backup_checkbox = QCheckBox("Enable Backup")
        vbox.addWidget(self._enable_backup_checkbox)

    def __add_backup_count(self, vbox: QVBoxLayout) -> None:
        count_vbox = QVBoxLayout()
        count_vbox.setSpacing(5)
        backup_count_label = QLabel("Backup Count")
        self._backup_count_spin_box = QSpinBox()
        count_vbox.addWidget(backup_count_label)
        count_vbox.addWidget(self._backup_count_spin_box)
        vbox.addLayout(count_vbox)

    def __add_backup_path(self, vbox: QVBoxLayout) -> None:

        back_path_vbox = QVBoxLayout()
        back_path_vbox.setSpacing(5)
        back_path_vbox.setContentsMargins(0, 0, 0, 0)
        backup_path_label = QLabel("Backup Path")
        back_path_vbox.addWidget(backup_path_label)

        hbox = QHBoxLayout()
        self._back_path_line_edit = QLineEdit()
        hbox.addWidget(self._back_path_line_edit)
        back_path_vbox.addLayout(hbox)

        vbox.addLayout(back_path_vbox)

    def __add_backup_list(self, vbox: QVBoxLayout) -> None:
        list_vbox = QVBoxLayout()
        list_vbox.setSpacing(5)
        backup_list_label = QLabel("Backup List")
        self._back_list_widget = ClickableListWidget()
        list_vbox.addWidget(backup_list_label)
        list_vbox.addWidget(self._back_list_widget)
        vbox.addLayout(list_vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    backup_tab = BackupTab(get_test_vocab_builder_db())
    backup_tab.show()
    sys.exit(app.exec_())
