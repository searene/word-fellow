import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QHBoxLayout, QSpinBox, \
    QApplication, QListWidgetItem, QFileDialog, QPushButton

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.ui.dialog.context.list.ClickableListWidget import ClickableListWidget
from vocab_builder.ui.widget.ClickableLineEdit import ClickableLineEdit


class BackupTab(QWidget):
    def __init__(self, backup_service: BackupService):
        super(BackupTab, self).__init__()
        self.__backup_service = backup_service
        self.__setup_ui()

    def __setup_ui(self) -> None:
        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        self.__add_enable_backup_checkbox(vbox)
        self.__add_backup_count(vbox)
        self.__add_backup_path(vbox)
        self.__add_backup_list(vbox)
        self.__update_ui()
        self.setLayout(vbox)
        
    def __update_ui(self) -> None:
        backup_config = self.__backup_service.get_backup_config()
        self._enable_backup_checkbox.setChecked(backup_config.backup_enabled)
        self._backup_count_spin_box.setValue(backup_config.backup_count)
        self._backup_path_line_edit.setText(backup_config.backup_folder_path)
        
        for backup in self.__backup_service.get_backups():
            item = QListWidgetItem()
            item.setText(backup.get_backup_name())
            item.setData(QtCore.Qt.UserRole, backup.backup_path)
            self._backup_list_widget.addItem(item)

    def __add_enable_backup_checkbox(self, vbox: QVBoxLayout) -> None:
        self._enable_backup_checkbox = QCheckBox("Enable Backup")
        self._enable_backup_checkbox.stateChanged.connect(self.__on_backup_checkbox_changed)
        vbox.addWidget(self._enable_backup_checkbox)

    def __on_backup_checkbox_changed(self, new_state: int) -> None:
        self.__backup_service.update_backup_enabled(True if new_state == Qt.CheckState.Checked else False)

    def __add_backup_count(self, vbox: QVBoxLayout) -> None:
        count_vbox = QVBoxLayout()
        count_vbox.setSpacing(5)
        backup_count_label = QLabel("Backup Count")
        self._backup_count_spin_box = QSpinBox()
        self._backup_count_spin_box.valueChanged.connect(self.__on_backup_count_spin_box_value_changed)
        count_vbox.addWidget(backup_count_label)
        count_vbox.addWidget(self._backup_count_spin_box)
        vbox.addLayout(count_vbox)

    def __on_backup_count_spin_box_value_changed(self, new_value: int) -> None:
        self.__backup_service.update_backup_count(new_value)

    def __add_backup_path(self, vbox: QVBoxLayout) -> None:

        back_path_vbox = QVBoxLayout()
        back_path_vbox.setSpacing(5)
        back_path_vbox.setContentsMargins(0, 0, 0, 0)
        backup_path_label = QLabel("Backup Path")
        back_path_vbox.addWidget(backup_path_label)

        hbox = QHBoxLayout()
        self._backup_path_line_edit = QLineEdit(self)
        self._backup_path_line_edit.setReadOnly(True)
        self._change_path_btn = QPushButton("Change")
        self._change_path_btn.clicked.connect(self.__on_change_path_btn_clicked)
        hbox.addWidget(self._backup_path_line_edit)
        hbox.addWidget(self._change_path_btn)
        back_path_vbox.addLayout(hbox)

        vbox.addLayout(back_path_vbox)

    def __on_change_path_btn_clicked(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Backup Folder", self._backup_path_line_edit.text())
        if path:
            self._backup_path_line_edit.setText(path)
            self.__backup_service.update_backup_folder_path(path)

    def __on_backup_path_line_edit_text_changed(self, new_text: str) -> None:
        self.__backup_service.update_backup_folder_path(new_text)

    def __add_backup_list(self, vbox: QVBoxLayout) -> None:
        list_vbox = QVBoxLayout()
        list_vbox.setSpacing(5)
        backup_list_label = QLabel("Backup List")
        self._backup_list_widget = ClickableListWidget()
        list_vbox.addWidget(backup_list_label)
        list_vbox.addWidget(self._backup_list_widget)
        vbox.addLayout(list_vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = get_test_vocab_builder_db()
    settings_service = SettingsService(db)
    backup_service = BackupService(settings_service)
    backup_tab = BackupTab(backup_service)
    backup_tab.show()
    sys.exit(app.exec_())
