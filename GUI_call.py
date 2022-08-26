from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem,  QPushButton, QTreeWidget, QLineEdit, QCheckBox, QStatusBar, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QFont
import sys
import exifread
import os
import logging
from datetime import datetime as dt
# from File_manag import *

logging.basicConfig(level=logging.ERROR)

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
		self.label_B = self.findChild(QLabel, "label_B")

		self.path_label_A = self.findChild(QLabel, "path_label_A")
		self.path_label_B = self.findChild(QLabel, "path_label_B")

		self.browse_A = self.findChild(QPushButton, "Browse_A")
		self.browse_B = self.findChild(QPushButton, "Browse_B")
		self.display_files_A = self.findChild(QPushButton, "display_files_A")
		self.display_files_B = self.findChild(QPushButton, "display_files_B")
		self.find_dup = self.findChild(QPushButton, "find_duplicates")
		self.delete_A = self.findChild(QPushButton, "delete_A")
		self.delete_B = self.findChild(QPushButton, "delete_B")

		self.subf_check_A = self.findChild(QCheckBox, "subfolders_A")
		self.subf_check_B = self.findChild(QCheckBox, "subfolders_B")
		self.exif_check_A = self.findChild(QCheckBox, "find_EXIF_A")
		self.exif_check_B = self.findChild(QCheckBox, "find_EXIF_B")

		self.statusBar = self.findChild(QStatusBar, "statusbar")
		self.statusBar.setFont(QFont("Arial", 18))

		self.tree_A = self.findChild(QTreeWidget, "tree_A")
		self.tree_B = self.findChild(QTreeWidget, "tree_B")


		# Acctions
		self.browse_A.clicked.connect(lambda x: self.browse("A"))  # Browse button A clicked
		self.browse_B.clicked.connect(lambda x: self.browse("B"))  # Browse button B clicked
		self.display_files_A.clicked.connect(lambda x: self.walk_folders("A") if self.clear_tree("A") == True else self.clear_tree("A") )
		self.display_files_A.clicked.connect(lambda x: self.clear_tree("B"))

		# self.find_dup.clicked.connect(lambda x: self.browse("A"))  # Find duplicates button clicked
		# self.delete_A.clicked.connect(lambda x: self.browse("B"))  # Delete from location A button clicked
		# self.delete_B.clicked.connect(lambda x: self.browse("B"))  # Delete from location B button clicked

		self.path_label_A.setText("C:/TEMP")
		self.path_label_B.setText("C:/TEMP")

		# Showing the App
		self.show()


	def browse(self, side):
		"""Opens dialog selecting folder location"""

		self.side = side
		dialog = QFileDialog(self)
		dialog.setDirectory(self.path_label_A.text()) if side == "A" else dialog.setDirectory(self.path_label_B.text())
		path = dialog.getExistingDirectory()
		self.displ_path(path)


	def displ_path(self, path):
		"""Display selected path in corresponding label"""

		self.path_label_A.setText(path) if self.side == "A" else self.path_label_B.setText(path)  # Display to tree A or B


	def clear_tree(self, side):


		self.side = side
		if self.side == "A":
			self.tree_A.clear()
		else:
			self.tree_B.clear()

		items = [QTreeWidgetItem(["Wait...................."])]
		self.tree_A.insertTopLevelItems(0, items)
		return True


	def walk_folders(self, side):
		"""WALKING THROUGH ALL FILES IN FOLDER AND SUB FOLDERS"""

		items = []
		self.side = side

		# self.clear_tree()

		if side == "A":   # reads path from label
			path = self.path_label_A.text()
		else:
			path = self.path_label_B.text()

		for path, subdirs, files in os.walk(path):
			for item in os.scandir(path):
				if item.is_file():
					path = item.path
					date = self.oldest_date(path)
					name = item.name
					file_type = os.path.splitext(item)[1]
					file_date = self.dateformat(self.ts_to_dt(item.stat().st_atime))
					size = ("{:,.0f} KB".format(item.stat().st_size / 1000).replace(",", " "))

					items.append(QTreeWidgetItem([name, file_type, size, date, path]))
		print(items)
		self.show_files(items)


	def show_files(self, items):
		"""Display files in corresponding tree and count in label"""

		if self.side == "A":  # Display to tree A or B
			self.tree_A.clear()
			self.tree_A.insertTopLevelItems(0, items)
			self.label_A.setText("{} files found".format(self.tree_A.topLevelItemCount()))
		else:
			self.tree_B.clear()
			self.tree_B.insertTopLevelItems(0, items)
			self.label_B.setText("{} files found".format(self.tree_B.topLevelItemCount()))


	def ts_to_dt(self, ts):
		return dt.fromtimestamp(ts)

	def dateformat(self, date_string):
		date_string = date_string.strftime("%Y.%m.%d %H:%M:%S")
		return date_string

	def oldest_date(self, path):
		"""EXTRACT 3 PICTURE CREATION DATES AND RETURNS THE OLDEST ONE"""
		print("AAAA" , self.exif_check_A.checkState())

		date_m = self.dateformat(self.ts_to_dt(os.path.getmtime(path)))  # Modification date
		date_c = self.dateformat(self.ts_to_dt(os.path.getctime(path)))  # File creation date

		if self.side == "A" and self.exif_check_A.checkState() or self.side == "B" and self.exif_check_B.checkState():

			# reading EXIF date
			try:
				file = open(path, 'rb')  # opens file to check if EXIF tag is there with date of picture taken
				tags = exifread.process_file(file, stop_tag="EXIF DateTimeOriginal")
				date_exif = str(tags["EXIF DateTimeOriginal"])  # Picture taken date
			except:
				date_exif = "Z"
				pass
			else:
				date_exif = date_exif[:4] + "." + date_exif[5:7] + "." + date_exif[8:] + "EXIF"  # replacing ':' with '.' in date format
			date = sorted([date_exif, date_c, date_m])[0]  # Selecting the oldest date

		else:
			date = sorted([date_c, date_m])[0]
		self.statusBar.showMessage("checked?  {}".format(date))
		return date




	def clicker(self, checked):
		self.label_A.setText("Clicked")
		print(self.path_line_A.text())
		self.path_line_A.clear()
		self.path_line_A.setText("Dupa")

		self.path_line_A.setClearButtonEnabled(True)



# initialize The App
app = QApplication(sys.argv)
UIWindow = MyWindow()
app.exec_()
print("DUpa")
