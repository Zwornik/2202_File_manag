from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets

import sys, os, logging, exifread, time, itertools
from datetime import datetime as dt


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        """Set up interface and all Widgets"""

        # Load interface from .ui file
        uic.loadUi("GUI_model.ui", self)
        # Set the main window icon
        appIcon = QIcon("Image\MK_ico.png")
        self.setWindowIcon(appIcon)

        # Variables
        self.no_warn = False  # True if time warning dialog window should not appear again
        self.init_img = "Tlo.jpg"
        self.sub_yes = False  # True if walk through files should include sub folders
        self.path = "C:/TEMP"
        self.canceled = False

        # Define data models

        self.model_A = QFileSystemModel()
        self.model_A.setRootPath(QDir.currentPath())
        self.model_B = QFileSystemModel()
        self.model_B.setRootPath(QDir.currentPath())

        # Define main window Widgets
        self.central_widget = self.findChild(QWidget, "centralwidget")

        self.tree_A = self.findChild(QTreeView, "tree_A")
        self.tree_B = self.findChild(QTreeView, "tree_B")

        self.splitter_2 = self.findChild(QSplitter, "splitter_2")
        self.splitter_2.setStretchFactor(0, 1)  # Make image area NOT resizing with main window

        self.summary_label_A = self.findChild(QLabel, "label_A")
        self.summary_label_B = self.findChild(QLabel, "label_B")

        self.path_label_A = self.findChild(QLabel, "path_label_A")
        self.path_label_B = self.findChild(QLabel, "path_label_B")

        self.image_label = self.findChild(QLabel, "image_view")
        self.image_label.resize(80, 2000)

        self.browse_btn_A = self.findChild(QPushButton, "Browse_A")
        self.browse_btn_B = self.findChild(QPushButton, "Browse_B")
        self.display_files_btn_A = self.findChild(QPushButton, "display_files_A")
        self.display_files_btn_B = self.findChild(QPushButton, "display_files_B")
        self.cancel_btn_A = self.findChild(QPushButton, "cancel_A")
        self.cancel_btn_B = self.findChild(QPushButton, "cancel_B")
        self.cancel_btn_A.setEnabled(False)  # Freeze buttons
        self.cancel_btn_B.setEnabled(False)

        self.find_duplicates_btn = self.findChild(QPushButton, "find_duplicates")
        self.delete_btn_A = self.findChild(QPushButton, "delete_A")
        self.delete_btn_B = self.findChild(QPushButton, "delete_B")

        MyWindow.subf_check_A = self.findChild(QCheckBox, "subfolders_A")
        MyWindow.subf_check_B = self.findChild(QCheckBox, "subfolders_B")
        MyWindow.exif_check_A = self.findChild(QCheckBox, "find_EXIF_A")
        MyWindow.exif_check_B = self.findChild(QCheckBox, "find_EXIF_B")

        # Assign data models to trees
        self.tree_A.setModel(self.model_A)
        self.tree_A.setRootIndex(self.model_A.index(self.path_label_A.text()))
        self.tree_B.setModel(self.model_B)
        self.tree_B.setRootIndex(self.model_B.index(self.path_label_B.text()))

        # Status bar settings
        self.statusBar = self.findChild(QStatusBar, "statusbar")
        status_font = QFont("Shell", 12, -1, True)
        status_font.setStretch(120)
        self.statusBar.setFont(status_font)
        self.statusBar.setStyleSheet("QStatusBar{padding-left:20px;color:rgb(216,5,5);font-weight:None}")

        # Acctions
        self.browse_btn_A.clicked.connect(lambda: self.browse("A"))  # 'Browse' button A clicked
        self.browse_btn_B.clicked.connect(lambda: self.browse("B"))  # 'Browse' button B clicked
        self.display_files_btn_A.clicked.connect(lambda: self.display_folder("A"))  # 'Display files' in tree 'A'
        self.display_files_btn_B.clicked.connect(lambda: self.display_folder("B"))  # 'Display files' in tree 'B'
        # self.cancel_btn_A.clicked.connect(self.cancel_it)  # 'Cancel' file search
        # self.cancel_btn_B.clicked.connect(self.cancel_it)  # 'Cancel' file search
        # self.tree_A.itemClicked.connect(self.select_img)
        # self.tree_B.itemClicked.connect(self.select_img)
        #
        # MyWindow.exif_check_A.toggled.connect(lambda: self.time_warning("A"))
        # MyWindow.exif_check_B.toggled.connect(lambda: self.time_warning("B"))
        # MyWindow.subf_check_A.toggled.connect(lambda: self.subforders("A"))
        # MyWindow.subf_check_B.toggled.connect(lambda: self.subforders("B"))

        # self.find_duplicates_btn.clicked.connect(self.both_folders_ok)  # Find duplicates button clicked
        self.delete_btn_A.clicked.connect(lambda x: self.browse("B"))  # Delete from location A button clicked
        self.delete_btn_B.clicked.connect(lambda x: self.browse("B"))  # Delete from location B button clicked
        # self.splitter_2.splitterMoved.connect(lambda: self.show_image(self.init_img))

        # GUI variables
        self.path_label_A.setText(self.path)
        self.path_label_B.setText(self.path)

        self.show()

    def browse(self, side):
        """Opens dialog for user to select folder location"""

        self.side = side
        dialog = QFileDialog(self)
        dialog.setDirectory(self.path_label_A.text()) if side == "A" else dialog.setDirectory(
            self.path_label_B.text())  # Set start Folder for dialog window
        path = dialog.getExistingDirectory()
        self.path_in_label(path)

    def path_in_label(self, path):
        """Display selected path in corresponding label"""

        self.path_label_A.setText(path) if self.side == "A" else self.path_label_B.setText(
            path)


    def display_folder(self, side):
        """Establish new thread and communication with it. Disable buttons
        variables:
        - side - determines on which side information is going to be displayed, obtained, widget activated
        - path - search path for files"""

        # self.disable_buttons(False)
        # self.clear_tree(side)

        if side == "A":  # Send 'path' and 'side' to 'Search_thread' class
            # self.tree_A.setModel(self.model_A)
            self.summary_label_A.setText("")
            path = self.path_label_A.text()  # Read PATH from label and send 'Search_thread.run' ????????
            self.model_A.setRootPath(path)
            self.tree_A.setRootIndex(self.model_A.index(path))
            self.tree_A.expandAll()
            self.tree_A.setSortingEnabled(True)

        else:
            self.summary_label_B.setText("")
            path = self.path_label_B.text()  # Variable to be read by 'Search_thread.run' ?????????
            self.model_B.setRootPath(path)
            self.tree_B.setRootIndex(self.model_B.index(path))
            self.tree_B.expandAll()
            self.tree_B.setSortingEnabled(True)
        print(path)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)  # Send select_img to pyqtSlot method to obtain selected item 'selected'
    def select_img(self, selected):
        """Obtains clicked image and send selected to be shown"""
        self.make_color(selected)
        print(selected.text(0), selected.text(4))
        img = selected.text(4)  # file path
        print(selected.text(0), selected.text(1), selected.text(2), selected.text(3), selected.text(4))
        # index =
        print(QtWidgets.indexOfChild(selected))
        self.init_img = img
        img.replace("/", "\\")
        self.show_image(img)

    def make_color(self, selected):
        font = QFont()
        font.setBold(True)
        color = QBrush(QColor(255, 130, 250))
        for i in range(5):
            # selected.setForeground(i, QBrush(QColor("red")))
            selected.setBackground(i, color)

    def get_files_no(self, side, path):  # ??????
        # and display in labels

        if side == "A":
            self.summary_label_A.setText(
                "{} files found".format(self.tree_A.topLevelItemCount()))
        else:
            self.summary_label_B.setText(
                "{} files found".format(self.tree_B.topLevelItemCount()))



    # def clear_tree(self, side):
    #     """Clear tree and display 'Wait...' in the tree"""
    #
    #     # ????? to be displayed between clearing and displaying?? items = [QTreeWidgetItem(["Wait, searching folder"])]
    #     if side == "A":
    #         self.tree_A.setModel(None)
    #         self.tree_A.setModel(self.model_A)
    #     else:
    #         self.tree_B.setModel(None)
    #         self.tree_B.setModel(self.model_B)


    # def disable_buttons(self, enable):
    #     """Enable / disable buttons when folders are scanned"""
    #
    #     print(enable)
    #     enable = True
    #     self.display_files_btn_A.setEnabled(enable)
    #     self.display_files_btn_B.setEnabled(enable)
    #     self.browse_btn_A.setEnabled(enable)
    #     self.browse_btn_B.setEnabled(enable)
    #     self.find_duplicates_btn.setEnabled(enable)
    #     self.delete_btn_A.setEnabled(enable)
    #     self.delete_btn_B.setEnabled(enable)
    #     MyWindow.exif_check_A.setEnabled(enable)
    #     MyWindow.exif_check_B.setEnabled(enable)
    #     MyWindow.subf_check_A.setEnabled(enable)
    #     MyWindow.subf_check_B.setEnabled(enable)






app = QApplication(sys.argv)
UIWindow = MyWindow()
app.exec_()