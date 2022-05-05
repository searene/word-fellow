import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QHBoxLayout, QSpinBox, \
    QApplication, QListWidgetItem, QFileDialog, QPushButton

from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.ui.dialog.context.list.ClickableListWidget import ClickableListWidget
from vocab_builder.ui.dialog.settings.backup.BackupDetailDialog import BackupDetailDialog
from vocab_builder.ui.util.DatabaseUtils import get_prod_vocab_builder_db


class BackupTab(QWidget):
    def __init__(self, backup_service: BackupService):
        super(BackupTab, self).__init__()
        self.__backup_service = backup_service
        self.__setup_ui()

    def __setup_ui(self) -> None:
        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        self.__add_tooltip(vbox)
        self.__add_enable_backup_checkbox(vbox)
        self.__add_backup_count(vbox)
        self.__add_backup_path(vbox)
        self.__add_backup_list(vbox)
        self._update_ui()
        self.setLayout(vbox)
        
    def _update_ui(self) -> None:
        backup_config = self.__backup_service.get_backup_config()
        self._enable_backup_checkbox.setChecked(backup_config.backup_enabled)
        self._backup_count_spin_box.setValue(backup_config.backup_count)
        self._backup_path_line_edit.setText(backup_config.backup_folder_path)
        self.__update_backup_list()
        
    def __update_backup_list(self):
        self._backup_list_widget.clear()
        for backup in self.__backup_service.get_backups():
            item = QListWidgetItem()
            item.setText(backup.get_backup_name())
            item.setData(QtCore.Qt.UserRole, backup.backup_path)
            item.setToolTip("Click to see details.")
            self._backup_list_widget.addItem(item)

    def __add_enable_backup_checkbox(self, vbox: QVBoxLayout) -> None:
        self._enable_backup_checkbox = QCheckBox("Enable Backup")
        self._enable_backup_checkbox.stateChanged.connect(self.__on_backup_checkbox_changed)
        vbox.addWidget(self._enable_backup_checkbox)

    def __on_backup_checkbox_changed(self, new_state: int) -> None:
        self.__backup_service.update_backup_enabled(new_state == Qt.Checked)
        self._backup_path_line_edit.setEnabled(new_state == Qt.Checked)
        self._backup_count_spin_box.setEnabled(new_state == Qt.Checked)
        self._backup_list_widget.setEnabled(new_state == Qt.Checked)

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
        self._backup_path_line_edit.textChanged.connect(self.__on_backup_path_changed)
        self._change_path_btn = QPushButton("Change")
        self._change_path_btn.clicked.connect(self.__on_change_path_btn_clicked)
        hbox.addWidget(self._backup_path_line_edit)
        hbox.addWidget(self._change_path_btn)
        back_path_vbox.addLayout(hbox)

        vbox.addLayout(back_path_vbox)

    def __on_backup_path_changed(self, new_path: str) -> None:
        self.__backup_service.update_backup_folder_path(new_path)
        self.__update_backup_list()

    def __on_change_path_btn_clicked(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Backup Folder", self._backup_path_line_edit.text())
        if not path:
            return
        self._backup_path_line_edit.setText(path)
        self._backup_path_line_edit.textChanged.emit(path)

    def __on_backup_path_line_edit_text_changed(self, new_text: str) -> None:
        self.__backup_service.update_backup_folder_path(new_text)

    def __add_backup_list(self, vbox: QVBoxLayout) -> None:
        list_vbox = QVBoxLayout()
        list_vbox.setSpacing(5)
        backup_list_label = QLabel("Backup List")
        self._backup_list_widget = ClickableListWidget()
        self._backup_list_widget.itemClicked.connect(self.__on_backup_list_item_clicked)
        list_vbox.addWidget(backup_list_label)
        list_vbox.addWidget(self._backup_list_widget)
        vbox.addLayout(list_vbox)

    def __on_backup_list_item_clicked(self, item: QListWidgetItem) -> None:
        backup = Backup(item.data(Qt.UserRole))
        self._backup_detail_dialog = BackupDetailDialog(self, backup, self.__backup_service)
        self._backup_detail_dialog.show()

    def __add_tooltip(self, vbox):
        label = QLabel("After enabling backup, your files will be backed up to the selected folder once a day.")
        vbox.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = get_prod_vocab_builder_db()
    settings_service = SettingsService(db)
    backup_service = BackupService(settings_service)
    backup_tab = BackupTab(backup_service)
    backup_tab.show()
    sys.exit(app.exec_())
