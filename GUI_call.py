# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidgetItem, QPushButton, QTreeWidget, \
# 	QCheckBox, QStatusBar, QFileDialog, QDialog, QDialogButtonBox, QSplitter, QWidget
# from PyQt5 import uic, QtCore, Qt
# from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, Qt
from PyQt5.QtCore import QThread, pyqtSignal

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets

import sys, os, logging, exifread, time
from datetime import datetime as dt

# from File_manag import *

logging.basicConfig(level=logging.ERROR)


class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()

		"""Set up interface and all Widgets"""

		# Load interface from .ui file
		uic.loadUi("GUI.ui", self)

		# Move main window to the center of the screen
		qtRectangle = self.frameGeometry()
		centerPiont = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPiont)
		self.move(qtRectangle.topLeft())

		# Set the main window icon
		appIcon = QIcon("Image\MK_ico.png")
		self.setWindowIcon(appIcon)

		# Variables
		self.no_warn = False  # True if time warning dialog window should not appear again
		self.init_img = "Tlo.jpg"
		self.sub_yes = False  # True if walk through files should include sub folders
		self.path = "C:/TEMP"

		# Second thread
		self.thread = Search_thread(self.path, self.sub_yes)

		# Define main window Widgets
		self.central_widget = self.findChild(QWidget, "centralwidget")

		self.label_A = self.findChild(QLabel, "label_A")
		self.label_B = self.findChild(QLabel, "label_B")

		self.path_label_A = self.findChild(QLabel, "path_label_A")
		self.path_label_B = self.findChild(QLabel, "path_label_B")

		self.image_label = self.findChild(QLabel, "image_view")
		self.image_label.resize(80,2000)

		self.browse_A = self.findChild(QPushButton, "Browse_A")
		self.browse_B = self.findChild(QPushButton, "Browse_B")
		self.display_files_A = self.findChild(QPushButton, "display_files_A")
		self.display_files_B = self.findChild(QPushButton, "display_files_B")
		self.cancel_A = self.findChild(QPushButton, "cancel_A")
		self.cancel_B = self.findChild(QPushButton, "cancel_B")
		self.cancel_A.setEnabled(False)  # Freeze buttons
		self.cancel_B.setEnabled(False)

		self.find_dup = self.findChild(QPushButton, "find_duplicates")
		self.delete_A = self.findChild(QPushButton, "delete_A")
		self.delete_B = self.findChild(QPushButton, "delete_B")

		MyWindow.subf_check_A = self.findChild(QCheckBox, "subfolders_A")
		MyWindow.subf_check_B = self.findChild(QCheckBox, "subfolders_B")
		MyWindow.exif_check_A = self.findChild(QCheckBox, "find_EXIF_A")
		MyWindow.exif_check_B = self.findChild(QCheckBox, "find_EXIF_B")

		self.statusBar = self.findChild(QStatusBar, "statusbar")
		self.statusBar.setFont(QFont("Arial", 18))

		self.tree_A = self.findChild(QTreeWidget, "tree_A")
		self.tree_B = self.findChild(QTreeWidget, "tree_B")

		self.splitter_2 = self.findChild(QSplitter, "splitter_2")
		self.splitter_2.setStretchFactor(0,1)  # Make image area NOT resizing with main window
		# class Handle(QWidget):
		# 	def paintEvent(self, e=None):
		# 		painter = QPainter(self)
		# 		painter.setPen(Qt.NoPen)
		# 		painter.setBrush(Qt.Dense6Pattern)
		# 		painter.drawRect(self.rect())
		#

		# # self.splitter_2.handle(1).setMaximumSize(5, 120)
		# l_handle = Handle()
		# self.splitter_2.addWidget(l_handle)
		# # self.splitter_2.setStyleSheet("QSplitter::handle {image: url(pus.png);}")
		# # self.splitter_2.setStyleSheet("QSplitter::handle:pressed {image: url(pushed.png);}")
		# # self.splitter_2.setStyleSheet("QSplitter::handle:setMaximumSize(3, 120);}")

		# Acctions
		self.browse_A.clicked.connect(lambda: self.browse("A"))  # 'Browse' button A clicked
		self.browse_B.clicked.connect(lambda: self.browse("B"))  # 'Browse' button B clicked
		self.display_files_A.clicked.connect(lambda: self.display_btn_clicked("A"))  # 'Display files' in tree 'A'
		self.display_files_B.clicked.connect(lambda: self.display_btn_clicked("B"))  # 'Display files' in tree 'B'
		self.cancel_A.clicked.connect(self.cancel_it)  # 'Cancel' file search
		self.cancel_B.clicked.connect(self.cancel_it)  # 'Cancel' file search
		self.tree_A.itemClicked.connect(self.select_img)
		self.tree_B.itemClicked.connect(self.select_img)
		# self.thread.progress.connect(lambda: print("OK"))
		# self.thread.finished.connect

		MyWindow.exif_check_A.toggled.connect(lambda: self.time_warning("A"))
		MyWindow.exif_check_B.toggled.connect(lambda: self.time_warning("B"))
		MyWindow.subf_check_A.toggled.connect(lambda: self.subforders("A"))
		MyWindow.subf_check_B.toggled.connect(lambda: self.subforders("B"))

		self.find_dup.clicked.connect(self.both_folders_ok)  # Find duplicates button clicked
		# self.delete_A.clicked.connect(lambda x: self.browse("B"))  # Delete from location A button clicked
		# self.delete_B.clicked.connect(lambda x: self.browse("B"))  # Delete from location B button clicked
		self.splitter_2.splitterMoved.connect(lambda: self.show_image(self.init_img))

		# GUI variables
		self.path_label_A.setText(self.path)
		self.path_label_B.setText(self.path)

		# self.image_label.

		# self.show_image()
		# Showing the App
		self.show()

	def subforders(self, side):
		if side == "A" and MyWindow.subf_check_A.checkState() or side == "B" and MyWindow.subf_check_B.checkState():
			self.sub_yes = True
			print(True)
		else:
			self.sub_yes = False
			print(False)


	def both_folders_ok(self):
		"""Check if both folders were selected"""
		if self.path_label_A.text() and self.path_label_B.text():
			print("Comapre trees")
		else:
			self.info_dialog("Please select folders for both locations")  # Show message in dialog window


	def info_dialog(self, message):
		"""Dialog window with message and 'OK' button"""

		info_dialog_obj = QDialog()
		uic.loadUi("Info_dialog.ui", info_dialog_obj)  # Loading UI file with Dialog
		glob = self.mapToGlobal(self.rect().center())  # Get coordinates of the center of main window
		info_dialog_obj.move(glob - info_dialog_obj.rect().center())  # Move Dialog to the center of main window

		button_OK = info_dialog_obj.findChild(QPushButton, "button_OK")
		button_OK.clicked.connect(lambda: info_dialog_obj.close())  # Close dialog when clicked

		info_label = info_dialog_obj.findChild(QLabel, "label")
		info_label.setText(message)  # Display message in the label

		x = info_dialog_obj.exec_()  # Show Dialog window


	@QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)  # Send select_img to pyqtSlot method to obtain selected item 'it'
	def select_img(self, it):
		"""Obtains clicked image and send it to be shown"""
		print(it.text(0), it.text(4))
		img = it.text(4)  # file path
		self.init_img = img
		img.replace("/","\\")
		self.show_image(img)

	def cancel_it(self):
		"""Cancel file walk when 'Cancel' btn is hit"""
		MyWindow.cancel = True
		self.cancel_A.setEnabled(False)
		self.cancel_B.setEnabled(False)
		print("CANCEL ", MyWindow.cancel)

	def show_image(self, img):
		"""Catch label size and display image in this size"""
		self.lbl_width = self.image_label.width()  # Catch current label dims
		self.lbl_height = self.image_label.height()

		self.image_label.resize(self.lbl_width, 2000)  # Resize label
		img_size = self.image_label.size()  # QSize object
		image = QPixmap(img).scaled(img_size, Qt.KeepAspectRatio)  # Assign image to QPixmap object with size and keep ratio
		self.image_label.setPixmap(image)  # Show image in the label

	def time_warning(self, side):
		"""Display time warning dialog"""
		MyWindow.side = side
		if self.no_warn is False and (side == "A" and MyWindow.exif_check_A.checkState() or \
		side == "B" and MyWindow.exif_check_B.checkState()):  # Verify if any of EXIF checkboxes is checked
			warning = QDialog()
			uic.loadUi("Time_warning.ui", warning)  # Loading UI file with Dialog
			glob = self.mapToGlobal(self.rect().center())  # Get coordinates of the center of main window
			warning.move(glob - warning.rect().center())  # Move Dialog to the center of main window
			button_box = warning.findChild(QDialogButtonBox, "buttonBox")
			self.warning_check_box = warning.findChild(QCheckBox, "checkBox")  # Create instance of 'no more warnings' check box

			button_box.accepted.connect(self.block_warning)
			button_box.rejected.connect(lambda: self.exif_check("Rejected"))

			x = warning.exec_()  # Show Dialog window

	def block_warning(self):
		"""Block time warning dialog from reappearing """
		if self.warning_check_box.checkState() == 2:  # Verify 'no more warnings' check box is checked
			self.no_warn = True  # Set not more warnings


	def exif_check(self, accept):
		"""Unchecks 'exif_check' box if 'cancel' selected in time warning window"""

		if MyWindow.side == "A":
			MyWindow.exif_check_A.setChecked(False)
		else:
			MyWindow.exif_check_B.setChecked(False)


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
		self.display_files_A.setEnabled(False)  # Freeze 'Display' buttons
		self.display_files_B.setEnabled(False)
		self.cancel_A.setEnabled(True)  # Unlock 'Cancel' buttons
		self.cancel_B.setEnabled(True)

		self.side = side

		if side == "A":  #Send 'path' and 'side' to 'Search_thread' class
			path = self.path_label_A.text()  # Read PATH from label and send 'Search_thread.run' ????????
			Search_thread.side = "A"  # Variable to be read by 'Search_thread.run'

		else:
			path = self.path_label_B.text()  # Variable to be read by 'Search_thread.run' ?????????
			Search_thread.side = "B"  # Variable to be read by 'Search_thread.run'

		self.thread = Search_thread(path, self.sub_yes)
		self.clear_tree()
		self.thread.start()
		self.thread.finished.connect(self.show_files)


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
		# Search_thread.quit()

		print("DISPLAYJJJJJJJJJJJJJJJJ")
		MyWindow.cancel = False
		# Search_thread.quit()

		if self.side == "A":  # Display to tree A or B

			self.tree_A.clear()
			self.tree_A.insertTopLevelItems(0, MyWindow.items)  # Variable set by 'Search_thread.run'
			self.label_A.setText("{} files found".format(self.tree_A.topLevelItemCount())) #Display items count in Label

		else:
			self.tree_B.clear()
			self.tree_B.insertTopLevelItems(0, MyWindow.items)  # Variable set by 'Search_thread.run'
			self.label_B.setText("{} files found".format(self.tree_B.topLevelItemCount())) #Display items count in Label

		self.display_files_A.setEnabled(True)  # Unfreeze buttons
		self.display_files_B.setEnabled(True)



"""""""""""""""""""   SECOND THREAD   """""""""""""""""""

class Search_thread(QThread):
	"""WALKING THROUGH ALL FILES IN FOLDER AND SUB FOLDERS"""
	finished = pyqtSignal()
	progress = pyqtSignal(int)
	MyWindow.cancel = False

	def __init__(self, path, sub_yes):
		super().__init__()
		self.path = path
		self.sub_yes = sub_yes
		print("Start path: ", path)
		MyWindow.items = []
	# path = MyWindow.path  # Variable set in display_btn_clicked
	# sub_yes = MyWindow.sub_yes

	def run(self):
		print("Start:  ", self.path)
		print("SUBS: ", self.sub_yes)
		print("Items: ", len(MyWindow.items))
		if MyWindow.cancel:
			return
		MyWindow.items = []

		def scan():
			with os.scandir(self.path) as folder:
				print(folder)
				for item in folder:
					self.path = item.path
					if item.is_file():
						print("File path: ", self.path)
						self.get_file_data(item)
					elif item.is_dir() and self.sub_yes:
						print("Dir path: ", self.path)
						scan()
					if MyWindow.cancel:  # Stop if 'Cancel' button pushed #True
						MyWindow.items = []
						MyWindow.items.append(QTreeWidgetItem(["Canceled..."]))
						self.finished.emit()
						return
						# Search_thread.quit(self)
			# self.emit_finish()
			# Search_thread.quit(self)
			print("Items 2:  ", len(MyWindow.items), MyWindow.items)
			self.finished.emit()
			return

		if MyWindow.items != []:
			self.finished.emit()
			return
		scan()
		#
		# return scan()

	def emit_finish(self):
		print("FINISH !")
		MyWindow.cancel = False
		self.finished.emit()  # Emit signal about finished file walk
		# Search_thread.quit(self)
		# self.wait()

	def get_file_data(self, item):
		"""Extract data from a file in 'item' object"""
		date = self.oldest_date(self.path)
		path = item.path
		name = item.name
		file_type = os.path.splitext(item)[1]
		file_date = self.dateformat(self.ts_to_dt(item.stat().st_atime))
		size = ("{:,.0f} KB".format(item.stat().st_size / 1000).replace(",", " "))
		self.progress.emit(2)
		MyWindow.items.append(QTreeWidgetItem([name, file_type, size, date, path]))

	# def walk(path, sub_yes):
	# 	with os.scandir(path) as folder:
	# 		for item in folder:
	# 			if sub_yes:
	# 				if item.is_dir():
	# 					path = item.path
	# 					print("path: ", path)
	# 					walk(path, sub_yes)
	# 				elif item.is_file:
	#
	# 					print(item.path)
	# 			else:
	# 				print(item.path)


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
				date_exif = "EXIF date unavailable"
				pass
			else:
				date_exif = date_exif.replace(":", ".", 2) + " EXIF"  # Format EXIF date

			date = sorted([date_exif, date_c, date_m])[0]  # Selecting the oldest date

		else:
			date = sorted([date_c, date_m])[0]

		return date


# self.statusBar.showMessage("checked?  {}".format(date))
	# return self.date


# initialize The App
app = QApplication(sys.argv)
UIWindow = MyWindow()
app.exec_()
