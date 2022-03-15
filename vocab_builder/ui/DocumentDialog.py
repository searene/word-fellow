from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox


class DocumentDialog(QDialog):

    def __init__(self, document_id: int, document_name: str):
        super(DocumentDialog, self).__init__()
        self.document_id = document_id
        self.document_name = document_name
        self.__init_ui()

    def show_dialog(self):
        self.show()
        self.exec_()

    def __init_ui(self):
        self.setWindowTitle(self.document_name)

        vbox = QVBoxLayout()
        vbox.addLayout(self.__get_top_bar())
        vbox.addLayout(self.__get_middle_area())
        vbox.addLayout(self.__get_bottom_bar())
        self.setLayout(vbox)

    def __get_top_bar(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(self.__get_status_combo_box())
        return hbox

    def __get_status_combo_box(self) -> QComboBox:
        status_combo_box = QComboBox()
        # TODO Fetch the list dynamically
        status_combo_box.addItem("Unknown")
        status_combo_box.addItem("Known")
        status_combo_box.addItem("Studying")
        return status_combo_box

    def __get_middle_area(self) -> QHBoxLayout:
        # TODO
        return QHBoxLayout()

    def __get_bottom_bar(self) -> QHBoxLayout:
        # TODO
        return QHBoxLayout()
