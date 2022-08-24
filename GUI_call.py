from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem,  QPushButton, QTreeWidget, QLineEdit, QCheckBox, QStatusBar, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QFont
import sys
# from File_manag import *


file_list = [('20160130_215245.jpg', '.jpg', '2 724', '2021.09.23 20:11:22', 'D:\\TEMP\\20160130_215245.jpg'), ('20160130_215331sadasdasdasdasdasdd.jpg', '.jpg', '2 689', '2022.08.18 16:26:14', 'D:\\TEMP\\20160130_215331sadasdasdasdasdasdd.jpg'), ('DSC_0044.JPG', '.JPG', '3 440', '2022.05.28 17:59:00', 'D:\\TEMP\\DSC_0044.JPG'), ('DSC_0044.NEF', '.NEF', '15 991', '2022.05.28 17:59:00', 'D:\\TEMP\\DSC_0044.NEF'), ('DSC_0045.JPG', '.JPG', '4 055', '2022.05.28 17:59:14', 'D:\\TEMP\\DSC_0045.JPG')]
item = ('20160130_215245.jpg', '.jpg', '2 724', '2021.09.23 20:11:22', 'D:\\TEMP\\20160130_215245.jpg')
Name = '20160130_215245.jpg'
Size = '2 724'
Path = 'D:\\TEMP\\20160130_215245.jpg'
items = []

class MyWindow(QMainWindow):

	def __init__(self):
		super(MyWindow, self).__init__()

		"""Set up interface and all Widegets"""

		self.setGeometry(200, 200, 600, 450)
		# Loadu .ui file
		uic.loadUi("GUI.ui", self)

		# Setting the main window icon
		appIcon = QIcon("Image\MK_ico.png")
		self.setWindowIcon(appIcon)

		# Define main window Widgets
		self.label_A = self.findChild(QLabel, "label_A")
		self.path_line_A = self.findChild(QLineEdit, "path_line_A")
		self.browse_A = self.findChild(QPushButton, "Browse_A")
		self.browse_B = self.findChild(QPushButton, "Browse_B")

		self.statusbBar = self.findChild(QStatusBar, "statusbar")
		self.statusbBar.setFont(QFont("Arial", 12))

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
		self.browse_A.clicked.connect(lambda x: self.browse("A")) # Button A
		self.browse_B.clicked.connect(lambda x: self.browse("B")) # Button B

		# self.clear.clicked.connect(self.clearer)

		# Showing the App
		self.show()


	def browse(self, side):
		"""Opens dialog selecting folder location"""

		dialog = QFileDialog(self)
		dialog.setDirectory("C:/")
		path = dialog.getExistingDirectory()
		self.show_files(self, path, side)


	def show_files(self, path, side):
		"""Display files from given folder in a tree"""

	def clear_tree(self, side):
		"""Clearing tree before loading data"""

		if side == "A":
			self.tree_A.clear()
		else:
			self.tree_B.clear()

	def
		# iterated through given location
		for fdata in path:
			# for i in fdata:
			name = fdata[0]
			ext = fdata[1]
			size = fdata[2]
			date = fdata[3]
			path = fdata[4]

			# create item to add to the tree
			item = QTreeWidgetItem([name, ext, size, date, path]) # accepts "" ot "","",""

	def display_tree(self, side):
		"""Display files in corresponding tree"""

		if side == "A":
			self.tree_A.insertTopLevelItems(0, [item])
		else:
			self.tree_B.insertTopLevelItems(0, [item])




	def clicker(self, checked):
		self.label_A.setText("Clicked")
		print(self.path_line_A.text())
		self.path_line_A.clear()
		self.path_line_A.setText("Dupa")
		self.statusbBar.showMessage("checked?  {}".format(checked))
		self.path_line_A.setClearButtonEnabled(True)

		# self.label_A.setText("Hello {}".format(self.path_line_A.toPlainText()))
		# self.label_A.adjustSize()
		# self.path_line_A.setPlainText("")

	# def clearer(self):
	# 	self.label.setText("Again, enter your name:")
	# 	self.textedit.setPlainText("")

	# def add(self, item):



# initialize The App
app = QApplication(sys.argv)
UIWindow = MyWindow()
app.exec_()