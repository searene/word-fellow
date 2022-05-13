from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class BackingUpDialog(QDialog):

    def __init__(self, parent=None):
        super(BackingUpDialog, self).__init__(parent)

        self.setWindowTitle("Backing Up...")

        self.__init_ui()

    def __init_ui(self):
        vbox = QVBoxLayout()

        desc_label = QLabel("It won't take more than 10 seconds, please wait for a while...")
        vbox.addWidget(desc_label)

        self.setLayout(vbox)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dlg = BackingUpDialog()
    dlg.show()

    sys.exit(app.exec_())