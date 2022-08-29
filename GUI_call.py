from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem, QPushButton, QTreeWidget, QLineEdit, \
	QCheckBox, QStatusBar, QFileDialog, QDialog, QDialogButtonBox
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QThread, pyqtSignal

import sys, time, os, logging, exifread
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

		# Variables
		self.no_warn = True  # False if time warning dialog window should not appear again


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
		MyWindow.exif_check_A = self.findChild(QCheckBox, "find_EXIF_A")
		MyWindow.exif_check_B = self.findChild(QCheckBox, "find_EXIF_B")

		self.statusBar = self.findChild(QStatusBar, "statusbar")
		self.statusBar.setFont(QFont("Arial", 18))

		self.tree_A = self.findChild(QTreeWidget, "tree_A")
		self.tree_B = self.findChild(QTreeWidget, "tree_B")

		# Acctions
		self.browse_A.clicked.connect(lambda: self.browse("A"))  # Browse button A clicked
		self.browse_B.clicked.connect(lambda: self.browse("B"))  # Browse button B clicked
		self.display_files_A.clicked.connect(lambda: self.display_btn_clicked("A"))
		self.display_files_B.clicked.connect(lambda: self.display_btn_clicked("B"))
		# Search_thread.progress.connect(self.label_A)

		MyWindow.exif_check_A.toggled.connect(lambda: self.time_warning("A"))
		MyWindow.exif_check_B.toggled.connect(lambda: self.time_warning("B"))
		# self.find_dup.clicked.connect(lambda x: self.browse("A"))  # Find duplicates button clicked
		# self.delete_A.clicked.connect(lambda x: self.browse("B"))  # Delete from location A button clicked
		# self.delete_B.clicked.connect(lambda x: self.browse("B"))  # Delete from location B button clicked

		self.path_label_A.setText("C:/TEMP")
		self.path_label_B.setText("C:/TEMP")

		# Showing the App
		self.show()

	def time_warning(self, side):
		"""Display warning dialog"""

		if self.no_warn and (MyWindow.exif_check_A.checkState() or MyWindow.exif_check_B.checkState()):  # Verify if any of checkboxes is checked
			warning = QDialog()
			uic.loadUi("Time_warning.ui", warning)  # Loading UI file with Dialog
			button_box = warning.findChild(QDialogButtonBox, "buttonBox")
			self.warning_check_box = warning.findChild(QCheckBox, "checkBox")

			self.warning_check_box.toggled.connect(self.block_warning)
			button_box.accepted.connect(lambda: self.exif_check("Accepted", side))
			button_box.rejected.connect(lambda: self.exif_check("Rejected", side))

			x = warning.exec_()  # Show Dialog window

	def block_warning(self):
		if self.warning_check_box.checkState() == 2:
			self.no_warn = False


	def exif_check(self, accept, side):
		"""Uncheck 'exif_check' check box if 'cancel' selected in warning window"""

		if accept == "Accepted":
			pass
		else:
			if side == "A":
				MyWindow.exif_check_A.setChecked(False)
				print("A False")
			else:
				MyWindow.exif_check_B.setChecked(False)
				print("B False")


	def browse(self, side):
		"""Opens dialog selecting folder location"""

		self.side = side
		dialog = QFileDialog(self)
		dialog.setDirectory(self.path_label_A.text()) if side == "A" else dialog.setDirectory(
				self.path_label_B.text())  # Set start Folder for dialog window
		path = dialog.getExistingDirectory()
		self.display_path(path)

	def display_path(self, path):
		"""Display selected path in corresponding label"""

		self.path_label_A.setText(path) if self.side == "A" else self.path_label_B.setText(path)  # Display path to tree A or B

	def display_btn_clicked(self, side):
		"""Establish new thread and communication with it
		variables:
		- side - determines on which side information is going to be displayed, obtained, widget activated
		- path - search path for files"""
		self.display_files_A.setEnabled(False)  # Freeze button
		self.display_files_B.setEnabled(False)  # Freeze button
		self.side = side

		if side == "A":  #Send 'path' and 'side' to 'Search_thread' class
			MyWindow.path = self.path_label_A.text()  # Variable to be read by 'Search_thread.run'
			MyWindow.side = "A"  # Variable to be read by 'Search_thread.run'

		else:
			MyWindow.path = self.path_label_B.text()  # Variable to be read by 'Search_thread.run'
			MyWindow.side = "B"  # Variable to be read by 'Search_thread.run'

		self.thread = Search_thread(self)
		self.thread.started.connect(self.clear_tree)
		self.thread.finished.connect(self.show_files)
		self.clear_tree()
		self.thread.start()

	def clear_tree(self):
		"""Clear tree and display 'Wait...' in the tree"""

		items = [QTreeWidgetItem(["Wait...................."])]
		if self.side == "A":
			self.tree_A.clear()
			self.tree_A.insertTopLevelItems(0, items)
		else:
			self.tree_B.clear()
			self.tree_B.insertTopLevelItems(0, items)

	def show_files(self):
		"""Display files in corresponding tree and count in label"""

		if self.side == "A":  # Display to tree A or B

			self.tree_A.clear()
			self.tree_A.insertTopLevelItems(0, Search_thread.items)  # Variable set by 'Search_thread.run'
			self.label_A.setText("{} files found".format(self.tree_A.topLevelItemCount())) #Display items count in Label

		else:
			self.tree_B.clear()
			self.tree_B.insertTopLevelItems(0, Search_thread.items)  # Variable set by 'Search_thread.run'
			self.label_B.setText("{} files found".format(self.tree_B.topLevelItemCount())) #Display items count in Label

		self.display_files_A.setEnabled(True)  # Unfreeze buttons
		self.display_files_B.setEnabled(True)


"""""""""""""""""""   SECOND THREAD   """""""""""""""""""

class Search_thread(QThread):
	"""WALKING THROUGH ALL FILES IN FOLDER AND SUB FOLDERS"""
	finished = pyqtSignal()
	progress = pyqtSignal(int)

	def run(self):

		self.path = MyWindow.path  # Variable set in display_btn_clicked
		self.side = MyWindow.side  # Variable set in display_btn_clicked

		Search_thread.items = []
		for path, subdirs, files in os.walk(self.path):
			for item in os.scandir(path):
				if item.is_file():
					path = item.path
					date = self.oldest_date(path)
					name = item.name
					file_type = os.path.splitext(item)[1]
					file_date = self.dateformat(self.ts_to_dt(item.stat().st_atime))
					size = ("{:,.0f} KB".format(item.stat().st_size / 1000).replace(",", " "))
					self.progress.emit(10)
					Search_thread.items.append(QTreeWidgetItem([name, file_type, size, date, path]))

		self.finished.emit()  # Emit signal about finished job

	def ts_to_dt(self, ts):
		"""Transform time stamp to datatime object"""
		return dt.fromtimestamp(ts)

	def dateformat(self, date_string):
		"""Format date string"""
		date_string = date_string.strftime("%Y.%m.%d %H:%M:%S")
		return date_string

	def oldest_date(self, path):
		"""EXTRACT 3 PICTURE CREATION DATES AND RETURNS THE OLDEST ONE"""

		# print(self.exif_check_A.checkState())
		date_m = self.dateformat(self.ts_to_dt(os.path.getmtime(path)))  # Modification date
		date_c = self.dateformat(self.ts_to_dt(os.path.getctime(path)))  # File creation date

		if self.side == "A" and MyWindow.exif_check_A.checkState() or self.side == "B" and MyWindow.exif_check_B.checkState():

			# reading EXIF date
			try:
				file = open(path, 'rb')  # opens file to check if EXIF tag is there with date of picture taken
				tags = exifread.process_file(file, stop_tag="EXIF DateTimeOriginal")
				date_exif = str(tags["EXIF DateTimeOriginal"])  # Picture taken date
			except:
				date_exif = "Z"
				pass
			else:
				date_exif = date_exif[:4] + "." + date_exif[5:7] + "." + date_exif[8:] + " exif"  # replacing ':' with '.' in date format
			date = sorted([date_exif, date_c, date_m])[0]  # Selecting the oldest date

		else:
			date = sorted([date_c, date_m])[0]

		return date

	# self.statusBar.showMessage("checked?  {}".format(date))
	# return self.date

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
