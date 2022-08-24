from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem,  QPushButton, QTreeWidget, QLineEdit, QCheckBox, QStatusBar, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QFont
import sys
import exifread
import os
import logging
from datetime import datetime as dt
# from File_manag import *


# file_list = [('20160130_215245.jpg', '.jpg', '2 724', '2021.09.23 20:11:22', 'D:\\TEMP\\20160130_215245.jpg'), ('20160130_215331sadasdasdasdasdasdd.jpg', '.jpg', '2 689', '2022.08.18 16:26:14', 'D:\\TEMP\\20160130_215331sadasdasdasdasdasdd.jpg'), ('DSC_0044.JPG', '.JPG', '3 440', '2022.05.28 17:59:00', 'D:\\TEMP\\DSC_0044.JPG'), ('DSC_0044.NEF', '.NEF', '15 991', '2022.05.28 17:59:00', 'D:\\TEMP\\DSC_0044.NEF'), ('DSC_0045.JPG', '.JPG', '4 055', '2022.05.28 17:59:14', 'D:\\TEMP\\DSC_0045.JPG')]
item = ('20160130_215245.jpg', '.jpg', '2 724', '2021.09.23 20:11:22', 'D:\\TEMP\\20160130_215245.jpg')
Name = '20160130_215245.jpg'
Size = '2 724'
Path = 'D:\\TEMP\\20160130_215245.jpg'
items = []
c=0

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
		self.tree_A.insertTopLevelItems(0, [item])

		# Tree B
		self.tree_B = self.findChild(QTreeWidget, "tree_B")
		item = QTreeWidgetItem([Name])
		Siz = QTreeWidgetItem([Size])
		item.addChild(Siz)
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
		print(path)
		self.walk_folders(path)


	def show_files(self, file_list):
		"""Display files in corresponding tree"""
		print("aaaaaaaaaaaaaa", file_list)
		items = []
		# side = 0
		# if side == "A":
		# 	self.tree_A.clear()
		# 	self.tree_A.insertTopLevelItems(items)
		# else:
		self.tree_B.clear()
		for i in file_list:
			items.append(QTreeWidgetItem(i))
		print(items)
		self.tree_B.insertTopLevelItems(0, items)

	def ts_to_dt(self, ts):
		return dt.fromtimestamp(ts)

	def dateformat(self, date_string):
		date_string = date_string.strftime("%Y.%m.%d %H:%M:%S")
		return date_string

	def oldest_date(self, path, date_extract):
		"""EXTRACTING 3 PICTURE CREATION DATES AND RETURNS THE OLDEST ONE"""

		date_m = self.dateformat(self.ts_to_dt(os.path.getmtime(path)))  # Modification date
		date_c = self.dateformat(self.ts_to_dt(os.path.getctime(path)))  # File creation date

		if date_extract == "Y":

			# reading EXIF date from picture reader
			try:
				file = open(path, 'rb')  # opens file to check if EXIF tag is there with date of picture taken
				tags = exifread.process_file(file, stop_tag="EXIF DateTimeOriginal")
				date_t = str(tags["EXIF DateTimeOriginal"])  # Picture taken date
			except:
				date_t = "Z"
				pass
			else:
				date_t = date_t[:4] + "." + date_t[5:7] + "." + date_t[8:]  # replacing : with . in date format
			date = sorted([date_t, date_c, date_m])[0]  # Selecting the oldest date

		else:
			date = sorted([date_c, date_m])[0]
		return date

	def walk_folders(self, path):
		"""WALKING THROUGH ALL FILES IN FOLDER AND SUB FOLDERS"""
		print(path)
		file_list = []
		for path, subdirs, files in os.walk(path):
			for item in os.scandir(path):
				if item.is_file():
					# self.c += 1
					path = item.path
					date = self.dateformat(self.ts_to_dt(os.path.getctime(path)))
					name = item.name
					file_type = os.path.splitext(item)[1]
					file_date = self.dateformat(self.ts_to_dt(item.stat().st_atime))
					size = ("{:,.0f}".format(item.stat().st_size / 1000).replace(",", " "))

					file_list.append([name, file_type, size, date, path])


			# print("{:<30s}   {}  {:>12} KB   {}   {}".format(name, file_type, size, date, path))

			# print(type(name), type(file_type), type(size), type(file_date), type(date), type(path))
		print(file_list)
		self.show_files(file_list)




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