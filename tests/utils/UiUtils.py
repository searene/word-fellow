from PyQt5.QtWidgets import QListWidget, QListWidgetItem


def get_visible_items(list_widget: QListWidget) -> [QListWidgetItem]:
    rect = list_widget.viewport().contentsRect()
    top = list_widget.indexAt(rect.topLeft())
    result = []
    if top.isValid():
        bottom = list_widget.indexAt(rect.bottomLeft())
        if not bottom.isValid():
            bottom = list_widget.model().index(list_widget.count() - 1, 0)
        for index in range(top.row(), bottom.row() + 1):
            result.append(list_widget.item(index))
    return result
