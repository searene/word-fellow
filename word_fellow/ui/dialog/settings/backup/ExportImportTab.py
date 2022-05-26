from typing import Optional

from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, \
    QMessageBox

from .....domain.export.ExportService import ExportService
from .....domain.export.ImportService import ImportService
from .....infrastructure import WordFellowDB
from .....ui.common.ClickableLineEdit import ClickableLineEdit
from .....ui.util import MsgUtils
from .....ui.util.DatabaseUtils import get_test_word_fellow_db


class ExportImportTab(QWidget):

    def __init__(self, parent: Optional[QWidget], db: WordFellowDB, show_ui=True):
        super().__init__(parent)
        self.__show_ui = show_ui
        self.__export_service = ExportService(db)
        self.__import_service = ImportService(db)
        self.__setup_ui()

    def __setup_ui(self):
        export_group = self.__get_export_group()
        import_group = self.__get_import_group()

        vbox = QVBoxLayout()
        vbox.addWidget(export_group)
        vbox.addWidget(import_group)
        self.setLayout(vbox)

    def __get_import_group(self) -> QGroupBox:
        hbox = QHBoxLayout()

        import_group = QGroupBox("Import")
        import_group.setLayout(hbox)

        self._import_line_edit = ClickableLineEdit(import_group)
        self._import_line_edit.setPlaceholderText("Click here to choose the import file...")
        self._import_line_edit.setReadOnly(True)
        self._import_line_edit.clicked.connect(self.__on_import_line_edit_clicked)

        self._import_btn = QPushButton(import_group)
        self._import_btn.clicked.connect(self.__on_import_btn_clicked)
        self._import_btn.setText("Import")
        hbox.addWidget(self._import_line_edit)
        hbox.addWidget(self._import_btn)

        return import_group

    def __on_import_btn_clicked(self):
        import_file_path = self._import_line_edit.text()
        is_valid, invalid_reason = self.__import_service.is_import_file_valid(import_file_path)
        if is_valid:
            self._import_warning_msg_box = QMessageBox(self)
            self._import_warning_msg_box.setIcon(QMessageBox.Warning)
            self._import_warning_msg_box.setText("Importing will overwrite the current Word Fellow data. Are you sure?")
            self._import_warning_msg_box.setWindowTitle("Warning")
            self._import_warning_msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            self._import_warning_msg_box.buttonClicked.connect(lambda btn: self.__on_import_msg_box_btn_clicked(btn, self._import_warning_msg_box))
            if self.__show_ui:
                self._import_warning_msg_box.exec()
        else:
            MsgUtils.show_warning_with_ok_btn(self, "Import failed", invalid_reason, show_ui=self.__show_ui)

    def __on_import_msg_box_btn_clicked(self, btn: QPushButton, msg_box: QMessageBox):
        btn_code = msg_box.standardButton(btn)
        if btn_code == QMessageBox.Ok:
            self.__import_service.do_import(self._import_line_edit.text())
            msg_box.close()
            self._import_success_msg_box = MsgUtils.show_info_with_ok_btn(self, "Import Successful", "Import Successful, please restart Anki to take effect.", show_ui=self.__show_ui)

    def __on_import_line_edit_clicked(self):
        import_file_path = QFileDialog.getOpenFileName(self, "Select Import File", self._import_line_edit.text(),
                                                       "Database files (*.db)")[0]
        if import_file_path:
            self._import_line_edit.setText(import_file_path)

    def __get_export_group(self) -> QGroupBox:
        hbox = QHBoxLayout()

        export_group = QGroupBox("Export")
        export_group.setLayout(hbox)

        self._export_line_edit = ClickableLineEdit(export_group)
        self._export_line_edit.setPlaceholderText("Click here to set the exported file path...")
        self._export_line_edit.setReadOnly(True)
        self._export_line_edit.clicked.connect(self.__on_export_line_edit_clicked)

        self._export_btn = QPushButton(export_group)
        self._export_btn.setText("Export")
        self._export_btn.clicked.connect(self.__on_export_btn_clicked)
        hbox.addWidget(self._export_line_edit)
        hbox.addWidget(self._export_btn)

        return export_group

    def __on_export_btn_clicked(self):
        export_file_path = self._export_line_edit.text()
        is_valid, invalid_reason = self.__export_service.is_export_file_valid(export_file_path)
        if is_valid:
            self.__export_service.export(export_file_path)
            self._export_success_msg_box = MsgUtils.show_info_with_ok_btn(self, "Successful", "Export Successful.", show_ui=self.__show_ui)
        else:
            self._export_failed_msg_box = MsgUtils.show_warning_with_ok_btn(self, "Export failed", invalid_reason, show_ui=self.__show_ui)

    def __on_export_line_edit_clicked(self):
        export_file_path = QFileDialog.getSaveFileName(self, "Select Export Folder", self._export_line_edit.text(),
                                                       "Database files (*.db)")[0]
        if export_file_path:
            self._export_line_edit.setText(export_file_path)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()
    w = ExportImportTab(None, db)
    w.show()
    app.exec_()
    db.destroy()
