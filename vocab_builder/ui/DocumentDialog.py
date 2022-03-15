from PyQt5.QtWidgets import QDialog


class DocumentDialog(QDialog):

    def __init__(self, document_id: int, document_name: str):
        super(DocumentDialog, self).__init__()
        self.document_id = document_id
        self.document_name = document_name
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle(self.document_name)

    def show_dialog(self):
        self.show()
        self.exec_()
