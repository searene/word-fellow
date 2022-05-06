import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QApplication

from word_fellow.domain.word.WordValueObject import WordContext


class LongContextDialog(QDialog):

    def __init__(self, long_context: WordContext):
        super(LongContextDialog, self).__init__()
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.__long_context = long_context
        self.__init_ui(self.__long_context)

    def show_dialog(self):
        self.show()
        self.exec_()

    def close_dialog(self):
        self.close()

    def __init_ui(self, long_context: WordContext):
        vbox = QVBoxLayout()
        vbox.addWidget(self.__get_context_area(long_context))
        vbox.addLayout(self.__get_bottom_btn_area())
        self.setLayout(vbox)

    def __get_context_area(self, long_context: WordContext) -> QTextEdit:
        text_edit = QTextEdit()
        text_edit.setHtml(long_context.to_html(allow_multi_line=True))
        text_edit.setReadOnly(True)
        return text_edit

    def __get_bottom_btn_area(self) -> QHBoxLayout:
        res = QHBoxLayout()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close_dialog)
        res.addWidget(close_btn)

        return res


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LongContextDialog(WordContext("test", "this is a test.", 0))
    dialog.show()
    sys.exit(app.exec_())