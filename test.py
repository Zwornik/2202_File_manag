import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

data = {"Project A": ["file_a.py", "file_a.txt", "something.xls"],
        "Project B": ["file_b.csv", "photo.jpg"],
        "Project C": []}

app = QApplication(sys.argv)


tree = QTreeWidget()
tree.setColumnCount(4)
tree.setHeaderLabels(["Name", "Type", "2", "3"])

items = []
for key, values in data.items():
    item = QTreeWidgetItem([key])
    for value in values:
        ext = value.split(".")[-1].upper()
        child = QTreeWidgetItem([value, ext])
        item.addChild(child)
    print(type(items), items)
    items.append(item)

tree.insertTopLevelItems(0, items)

tree.show()
sys.exit(app.exec())