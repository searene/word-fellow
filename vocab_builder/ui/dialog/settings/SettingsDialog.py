from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget

from vocab_builder.ui.dialog.settings.BackupTab import BackupTab
from vocab_builder.ui.dialog.settings.ResetTab import ResetTab


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        self.setWindowTitle("Settings")
        vbox = QVBoxLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(BackupTab(), "Backup")
        tab_widget.addTab(ResetTab(), "Reset")
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = SettingsDialog()
    w.show()
    sys.exit(app.exec_())