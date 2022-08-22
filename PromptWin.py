from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QTreeWidgetItem,  QPushButton, QListWidget, QListView, QTreeWidget, QTreeView
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys

file_list = [('20160130_215245.jpg', '.jpg', '2 724', '2021.09.23 20:11:22', 'D:\\TEMP\\20160130_215245.jpg'), ('20160130_215331sadasdasdasdasdasdd.jpg', '.jpg', '2 689', '2022.08.18 16:26:14', 'D:\\TEMP\\20160130_215331sadasdasdasdasdasdd.jpg'), ('DSC_0044.JPG', '.JPG', '3 440', '2022.05.28 17:59:00', 'D:\\TEMP\\DSC_0044.JPG'), ('DSC_0044.NEF', '.NEF', '15 991', '2022.05.28 17:59:00', 'D:\\TEMP\\DSC_0044.NEF'), ('DSC_0045.JPG', '.JPG', '4 055', '2022.05.28 17:59:14', 'D:\\TEMP\\DSC_0045.JPG')]
item = ('20160130_215245.jpg', '.jpg', '2 724', '2021.09.23 20:11:22', 'D:\\TEMP\\20160130_215245.jpg')
Name = '20160130_215245.jpg'
Size = '2 724'
Path = 'D:\\TEMP\\20160130_215245.jpg'
items = []

class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setGeometry(200, 200, 600, 450)
		# Loadu .ui file
		uic.loadUi("PromptWin.ui", self)

	# def setIcon(self):
		appIcon = QIcon("MK_ico.png")
		self.setWindowIcon(appIcon)

		#Define Widgets
		self.label = self.findChild(QLabel, "label")
		self.textedit = self.findChild(QTextEdit, "textEdit")
		self.button =  self.findChild(QPushButton, "pushButton")
		self.clear = self.findChild(QPushButton, "pushButton_2")

		# Tree A
		self.tree_A = self.findChild(QTreeWidget, "tree_A")
		item = QTreeWidgetItem([Name])
		Siz = QTreeWidgetItem([Size])
		item.addChild(Siz)
		print(item, Siz,)
		self.tree_A.insertTopLevelItems(0, [item])

		# Tree B
		self.tree_B = self.findChild(QTreeWidget, "tree_B")
		item = QTreeWidgetItem([Name])
		Siz = QTreeWidgetItem([Size])
		item.addChild(Siz)
		print(item, Siz, )
		self.tree_B.insertTopLevelItems(0, [item])

		# Acctions
		# self.button.clicked.connect(self.clicker)
		# self.clear.clicked.connect(self.clearer)

		# Showing the App
		self.show()

	def clicker(self):
		self.label.setText("Hello {}".format(self.textedit.toPlainText()))
		self.label.adjustSize()
		self.textedit.setPlainText("")

	def clearer(self):
		self.label.setText("Again, enter your name:")
		self.textedit.setPlainText("")

	# def add(self, item):



# initialize The App
app = QApplication(sys.argv)
UIWindow = MyWindow()
app.exec_()