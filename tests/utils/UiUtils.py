from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget


def get_visible_item_indices(list_widget: QListWidget) -> [int]:
    rect = list_widget.viewport().contentsRect()
    top = list_widget.indexAt(rect.topLeft())
    result = []
    if top.isValid():
        bottom = list_widget.indexAt(rect.bottomLeft())
        if not bottom.isValid():
            bottom = list_widget.model().index(list_widget.count() - 1, 0)
        for index in range(top.row(), bottom.row() + 1):
            result.append(index)
    return result


def get_visible_items(list_widget: QListWidget) -> [QListWidgetItem]:
    return [list_widget.item(index) for index in get_visible_item_indices(list_widget)]


def get_visible_item_widgets(list_widget: QListWidget) -> [QWidget]:
    return [list_widget.itemWidget(item) for item in get_visible_items(list_widget)]