from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout

from word_fellow.domain.export.ExportService import ExportService
from word_fellow.domain.export.ImportService import ImportService
from word_fellow.infrastructure import WordFellowDB
from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db


class ExportImportTab(QWidget):

    def __init__(self, db: WordFellowDB):
        super().__init__()
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

        self._import_line_edit = QLineEdit(import_group)
        self._import_btn = QPushButton(import_group)
        self._import_btn.setText("Import")
        hbox.addWidget(self._import_line_edit)
        hbox.addWidget(self._import_btn)

        return import_group

    def __get_export_group(self) -> QGroupBox:
        hbox = QHBoxLayout()

        export_group = QGroupBox("Export")
        export_group.setLayout(hbox)

        self._export_line_edit = QLineEdit(export_group)
        self._export_btn = QPushButton(export_group)
        self._export_btn.setText("Export")
        hbox.addWidget(self._export_line_edit)
        hbox.addWidget(self._export_btn)

        return export_group


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()
    w = ExportImportTab(db)
    w.show()
    app.exec_()
    db.destroy()
