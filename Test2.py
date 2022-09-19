from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets


import sys, os, logging, exifread, time
from datetime import datetime as dt


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.path = "C:/TEMP"

        self.ddd = {"file1": [{'root':{'folder':'file1'}},'size', 'date', 'ext'],
                    'folder': [{'root': 'folder'},'', '', ''],
                    "file2": [{'root': "file2"}, 'size', 'date', 'ext'],
                    "file3": [{'root': {'folder': 'file3'}}, 'size', 'date', 'ext'],
        }

        self.d = {'TestName': {'Ref': 'ABC/DEF',
                               'Property': [{'Number': '2', 'Zipcode': '0002234','KeyAvailable': 'Yes'}, {'Number': '3',
                                                                                        'Zipcode': '2342444'}]}}

        self.dee = [[['dupa']], [['10_2 — kopia.jpg'], '10_2 — kopia.jpg', '.jpg', '15 526 KB', '2021.09.23 20:03:56'], [['20160130_215245.jpg'], '20160130_215245.jpg', '.jpg', '2 724 KB', '2021.09.23 20:11:22'], [['20160130_215331sadasdasdasdasdasdd.jpg'], '20160130_215331sadasdasdasdasdasdd.jpg', '.jpg', '2 689 KB', '2022.08.18 16:26:14'], [['aaaa']], [['aaaa',['10_3.jpg']], '10_3.jpg', '.jpg', '1 001 KB', '2021.09.23 20:03:56'], [['aaaa', ['12_1.jpg']], '12_1.jpg', '.jpg', '20 074 KB', '2021.09.23 20:03:57'], [['aaaa', ['12_2.jpg']], '12_2.jpg', '.jpg', '3 540 KB', '2021.09.23 20:03:57'], [['aaaa', ['20160127_032604.jpg']], '20160127_032604.jpg', '.jpg', '1 031 KB', '2021.09.23 20:11:22'], [['aaaa', ['20160130_215245.jpg']], '20160130_215245.jpg', '.jpg', '2 724 KB', '2021.09.23 20:11:22'], [['aaaa', ['20160130_215331.jpg']], '20160130_215331.jpg', '.jpg', '2 685 KB', '2021.09.23 20:11:22'], [['aaaa', ['Duży pokój']], [['aaaa', ['Duży pokój', ['P1040356.JPG']]], 'P1040356.JPG', '.JPG', '4 439 KB', '2022.08.17 09:59:00'], [['aaaa', ['Duży pokój', ['P1040371.JPG']]], 'P1040371.JPG', '.JPG', '4 603 KB', '2022.08.17 10:17:04'], [['aaaa', ['Duży pokój', ['P1040372.JPG']]], 'P1040372.JPG', '.JPG', '4 887 KB', '2022.08.17 10:25:54'], [['aaaa', ['Duży pokój', ['P1040373.JPG']]], 'P1040373.JPG', '.JPG', '4 968 KB', '2022.08.17 10:26:30'], [['aaaa', ['Duży pokój', ['P1040393.JPG']]], 'P1040393.JPG', '.JPG', '5 067 KB', '2022.08.17 10:52:28'], [['bbbbb']], [['bbbbb', ['10_2.jpg']], '10_2.jpg', '.jpg', '15 526 KB', '2021.09.23 20:03:56'], [['bbbbb', '12_1.jpg'], '12_1.jpg', '.jpg', '20 074 KB', '2021.09.23 20:03:57'], [['bbbbb', 'ccccc']], [['bbbbb', 'ccccc', '20160130_215245.jpg'], '20160130_215245.jpg', '.jpg', '2 724 KB', '2021.09.23 20:11:22'], [['bbbbb', 'ccccc', '20160130_215331.jpg'], '20160130_215331.jpg', '.jpg', '2 685 KB', '2021.09.23 20:11:22'], [['bbbbb', 'ccccc', 'Mały pokój']], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040273.JPG'], 'P1040273.JPG', '.JPG', '3 513 KB', '2022.08.17 07:37:24'], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040288.JPG'], 'P1040288.JPG', '.JPG', '3 693 KB', '2022.08.17 08:02:22'], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040294.JPG'], 'P1040294.JPG', '.JPG', '3 875 KB', '2022.08.17 08:06:40'], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040294a.JPG'], 'P1040294a.JPG', '.JPG', '4 816 KB', '2022.08.17 12:48:20'], [['cc']], [['dasds.dadasd']], [['DSC_0044.JPG'], 'DSC_0044.JPG', '.JPG', '3 440 KB', '2022.05.28 17:59:00'], [['DSC_0044.NEF'], 'DSC_0044.NEF', '.NEF', '15 991 KB', '2022.05.28 17:59:00'], [['DSC_0045.JPG'], 'DSC_0045.JPG', '.JPG', '4 055 KB', '2022.05.28 17:59:14'], [['DSC_0045.NEF'], 'DSC_0045.NEF', '.NEF', '16 564 KB', '2022.05.28 17:59:14'], [['dziś']], [['dziś', '20220829_130508.jpg'], '20220829_130508.jpg', '.jpg', '2 839 KB', '2022.08.29 13:05:10'], [['dziś', '20220829_130508a.jpg'], '20220829_130508a.jpg', '.jpg', '3 032 KB', '2022.08.29 15:27:24'], [['dziś', '20220829_130508b.jpg'], '20220829_130508b.jpg', '.jpg', '2 755 KB', '2022.08.29 15:28:30'], [['dziś', '20220829_130508c.jpg'], '20220829_130508c.jpg', '.jpg', '2 741 KB', '2022.08.29 15:29:08'], [['dziś', '20220829_130508d.jpg'], '20220829_130508d.jpg', '.jpg', '3 033 KB', '2022.08.29 14:00:42'], [['dziś', '20220829_130508_2.jpg'], '20220829_130508_2.jpg', '.jpg', '1 899 KB', '2022.08.29 16:06:24'], [['dziś', '20220829_130508_MK.jpg'], '20220829_130508_MK.jpg', '.jpg', '1 893 KB', '2022.08.29 16:07:27'], [['dziś', '20220829_131343.jpg'], '20220829_131343.jpg', '.jpg', '3 026 KB', '2022.08.29 13:13:46'], [['dziś', '20220829_131343a.jpg'], '20220829_131343a.jpg', '.jpg', '3 231 KB', '2022.08.29 15:25:38'], [['dziś', '20220829_134919.jpg'], '20220829_134919.jpg', '.jpg', '3 226 KB', '2022.08.29 13:49:24'], [['dziś', '20220829_135458.jpg'], '20220829_135458.jpg', '.jpg', '3 155 KB', '2022.08.29 13:55:02'], [['dziś', '20220829_151722.jpg'], '20220829_151722.jpg', '.jpg', '2 892 KB', '2022.08.29 15:17:26'], [['dziś', '20220829_151722a.jpg'], '20220829_151722a.jpg', '.jpg', '2 790 KB', '2022.08.29 13:33:00'], [['dziś', '20220829_151842.jpg'], '20220829_151842.jpg', '.jpg', '2 805 KB', '2022.08.29 15:18:46'], [['dziś', '20220829_151842_2.jpg'], '20220829_151842_2.jpg', '.jpg', '1 803 KB', '2022.08.29 16:17:31'], [['dziś', '20220829_153506.jpg'], '20220829_153506.jpg', '.jpg', '2 797 KB', '2022.08.29 15:35:08'], [['dziś', '20220829_153746.jpg'], '20220829_153746.jpg', '.jpg', '2 739 KB', '2022.08.29 15:37:50'], [['dziś', '20220829_154143.jpg'], '20220829_154143.jpg', '.jpg', '2 713 KB', '2022.08.29 15:41:46'], [['IMG_4117.jpeg'], 'IMG_4117.jpeg', '.jpeg', '357 KB', '2011.05.31 17:28:00'], [['IMG_4120.jpeg'], 'IMG_4120.jpeg', '.jpeg', '285 KB', '2022.08.20 16:01:55'], [['nnnn']], [['ok.psd'], 'ok.psd', '.psd', '340 KB', '2011.04.20 17:04:30'], [['P1031111.mp3'], 'P1031111.mp3', '.mp3', '5 521 KB', '2022.06.30 23:39:01'], [['P1040195.JPG'], 'P1040195.JPG', '.JPG', '6 544 KB', '2022.08.16 14:10:22'], [['P1040409.JPG'], 'P1040409.JPG', '.JPG', '3 988 KB', '2022.08.17 11:23:26'], [['P1040415.JPG'], 'P1040415.JPG', '.JPG', '4 375 KB', '2022.08.17 11:49:04'], [['P1040416.JPG'], 'P1040416.JPG', '.JPG', '6 544 KB', '2022.08.16 14:10:22'], [['P1040418.JPG'], 'P1040418.JPG', '.JPG', '4 242 KB', '2022.08.17 11:53:50'], [['received_1534376623278967.gif'], 'received_1534376623278967.gif', '.gif', '502 KB', '2021.09.23 20:05:32'], [['received_2018651381724765.gif'], 'received_2018651381724765.gif', '.gif', '446 KB', '2021.09.23 20:05:32'], [['Untitled-1.png'], 'Untitled-1.png', '.png', '4 674 KB', '2002.04.09 21:53:22'], [['Untitled-13.png'], 'Untitled-13.png', '.png', '4 601 KB', '2002.04.09 21:51:34'], [['Ushedshim slishkom rano.mp3'], 'Ushedshim slishkom rano.mp3', '.mp3', '5 236 KB', '2022.06.30 23:39:06'], [['Vesna.mp3'], 'Vesna.mp3', '.mp3', '7 226 KB', '2022.06.30 23:39:04'], [['Voda.mp3'], 'Voda.mp3', '.mp3', '5 532 KB', '2022.06.30 23:39:01'], [['WOL_MIESZKANIE 2020_14.skp'], 'WOL_MIESZKANIE 2020_14.skp', '.skp', '43 070 KB', '2022.06.02 09:06:42'], [['WOL_MODEL 1.skp'], 'WOL_MODEL 1.skp', '.skp', '25 108 KB', '2009.10.25 11:38:28'], [['ZAPROSZENIE.psd'], 'ZAPROSZENIE.psd', '.psd', '2 563 KB', '2011.04.14 22:46:34']]]
        self.ee = [[['.dupa']], [['10_2 — kopia.jpg'], '10_2 — kopia.jpg', '.jpg', '15 526 KB', '2021.09.23 20:03:56'], [['20160130_215245.jpg'], '20160130_215245.jpg', '.jpg', '2 724 KB', '2021.09.23 20:11:22'], [['20160130_215331sadasdasdasdasdasdd.jpg'], '20160130_215331sadasdasdasdasdasdd.jpg', '.jpg', '2 689 KB', '2022.08.18 16:26:14'], [['aaaa']], [['aaaa', '111111.jpg'], '10_3.jpg', '.jpg', '1 001 KB', '2021.09.23 20:03:56'], [['aaaa', '12_1.jpg'], '12_1.jpg', '.jpg', '20 074 KB', '2021.09.23 20:03:57'], [['aaaa', '12_2.jpg'], '12_2.jpg', '.jpg', '3 540 KB', '2021.09.23 20:03:57'], [['aaaa', '20160127_032604.jpg'], '20160127_032604.jpg', '.jpg', '1 031 KB', '2021.09.23 20:11:22'], [['aaaa', '20160130_215245.jpg'], '20160130_215245.jpg', '.jpg', '2 724 KB', '2021.09.23 20:11:22'], [['aaaa', '20160130_215331.jpg'], '20160130_215331.jpg', '.jpg', '2 685 KB', '2021.09.23 20:11:22'], [['aaaa', 'Duży pokój']], [['aaaa', 'Duży pokój', 'P1040356.JPG'], 'P1040356.JPG', '.JPG', '4 439 KB', '2022.08.17 09:59:00'], [['aaaa', 'Duży pokój', 'P1040371.JPG'], 'P1040371.JPG', '.JPG', '4 603 KB', '2022.08.17 10:17:04'], [['aaaa', 'Duży pokój', 'P1040372.JPG'], 'P1040372.JPG', '.JPG', '4 887 KB', '2022.08.17 10:25:54'], [['aaaa', 'Duży pokój', 'P1040373.JPG'], 'P1040373.JPG', '.JPG', '4 968 KB', '2022.08.17 10:26:30'], [['aaaa', 'Duży pokój', 'P1040393.JPG'], 'P1040393.JPG', '.JPG', '5 067 KB', '2022.08.17 10:52:28'], [['bbbbb']], [['bbbbb', '10_2.jpg'], '10_2.jpg', '.jpg', '15 526 KB', '2021.09.23 20:03:56'], [['bbbbb', '12_1.jpg'], '12_1.jpg', '.jpg', '20 074 KB', '2021.09.23 20:03:57'], [['bbbbb', 'ccccc']], [['bbbbb', 'ccccc', '20160130_215245.jpg'], '20160130_215245.jpg', '.jpg', '2 724 KB', '2021.09.23 20:11:22'], [['bbbbb', 'ccccc', '20160130_215331.jpg'], '20160130_215331.jpg', '.jpg', '2 685 KB', '2021.09.23 20:11:22'], [['bbbbb', 'ccccc', 'Mały pokój']], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040273.JPG'], 'P1040273.JPG', '.JPG', '3 513 KB', '2022.08.17 07:37:24'], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040288.JPG'], 'P1040288.JPG', '.JPG', '3 693 KB', '2022.08.17 08:02:22'], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040294.JPG'], 'P1040294.JPG', '.JPG', '3 875 KB', '2022.08.17 08:06:40'], [['bbbbb', 'ccccc', 'Mały pokój', 'P1040294a.JPG'], 'P1040294a.JPG', '.JPG', '4 816 KB', '2022.08.17 12:48:20'], [['cc']], [['dasds.dadasd']], [['DSC_0044.JPG'], 'DSC_0044.JPG', '.JPG', '3 440 KB', '2022.05.28 17:59:00'], [['DSC_0044.NEF'], 'DSC_0044.NEF', '.NEF', '15 991 KB', '2022.05.28 17:59:00'], [['DSC_0045.JPG'], 'DSC_0045.JPG', '.JPG', '4 055 KB', '2022.05.28 17:59:14'], [['DSC_0045.NEF'], 'DSC_0045.NEF', '.NEF', '16 564 KB', '2022.05.28 17:59:14'], [['dziś']], [['dziś', '20220829_130508.jpg'], '20220829_130508.jpg', '.jpg', '2 839 KB', '2022.08.29 13:05:10'], [['dziś', '20220829_130508a.jpg'], '20220829_130508a.jpg', '.jpg', '3 032 KB', '2022.08.29 15:27:24'], [['dziś', '20220829_130508b.jpg'], '20220829_130508b.jpg', '.jpg', '2 755 KB', '2022.08.29 15:28:30'], [['dziś', '20220829_130508c.jpg'], '20220829_130508c.jpg', '.jpg', '2 741 KB', '2022.08.29 15:29:08'], [['dziś', '20220829_130508d.jpg'], '20220829_130508d.jpg', '.jpg', '3 033 KB', '2022.08.29 14:00:42'], [['dziś', '20220829_130508_2.jpg'], '20220829_130508_2.jpg', '.jpg', '1 899 KB', '2022.08.29 16:06:24'], [['dziś', '20220829_130508_MK.jpg'], '20220829_130508_MK.jpg', '.jpg', '1 893 KB', '2022.08.29 16:07:27'], [['dziś', '20220829_131343.jpg'], '20220829_131343.jpg', '.jpg', '3 026 KB', '2022.08.29 13:13:46'], [['dziś', '20220829_131343a.jpg'], '20220829_131343a.jpg', '.jpg', '3 231 KB', '2022.08.29 15:25:38'], [['dziś', '20220829_134919.jpg'], '20220829_134919.jpg', '.jpg', '3 226 KB', '2022.08.29 13:49:24'], [['dziś', '20220829_135458.jpg'], '20220829_135458.jpg', '.jpg', '3 155 KB', '2022.08.29 13:55:02'], [['dziś', '20220829_151722.jpg'], '20220829_151722.jpg', '.jpg', '2 892 KB', '2022.08.29 15:17:26'], [['dziś', '20220829_151722a.jpg'], '20220829_151722a.jpg', '.jpg', '2 790 KB', '2022.08.29 13:33:00'], [['dziś', '20220829_151842.jpg'], '20220829_151842.jpg', '.jpg', '2 805 KB', '2022.08.29 15:18:46'], [['dziś', '20220829_151842_2.jpg'], '20220829_151842_2.jpg', '.jpg', '1 803 KB', '2022.08.29 16:17:31'], [['dziś', '20220829_153506.jpg'], '20220829_153506.jpg', '.jpg', '2 797 KB', '2022.08.29 15:35:08'], [['dziś', '20220829_153746.jpg'], '20220829_153746.jpg', '.jpg', '2 739 KB', '2022.08.29 15:37:50'], [['dziś', '20220829_154143.jpg'], '20220829_154143.jpg', '.jpg', '2 713 KB', '2022.08.29 15:41:46'], [['IMG_4117.jpeg'], 'IMG_4117.jpeg', '.jpeg', '357 KB', '2011.05.31 17:28:00'], [['IMG_4120.jpeg'], 'IMG_4120.jpeg', '.jpeg', '285 KB', '2022.08.20 16:01:55'], [['nnnn']], [['ok.psd'], 'ok.psd', '.psd', '340 KB', '2011.04.20 17:04:30'], [['P1031111.mp3'], 'P1031111.mp3', '.mp3', '5 521 KB', '2022.06.30 23:39:01'], [['P1040195.JPG'], 'P1040195.JPG', '.JPG', '6 544 KB', '2022.08.16 14:10:22'], [['P1040409.JPG'], 'P1040409.JPG', '.JPG', '3 988 KB', '2022.08.17 11:23:26'], [['P1040415.JPG'], 'P1040415.JPG', '.JPG', '4 375 KB', '2022.08.17 11:49:04'], [['P1040416.JPG'], 'P1040416.JPG', '.JPG', '6 544 KB', '2022.08.16 14:10:22'], [['P1040418.JPG'], 'P1040418.JPG', '.JPG', '4 242 KB', '2022.08.17 11:53:50'], [['received_1534376623278967.gif'], 'received_1534376623278967.gif', '.gif', '502 KB', '2021.09.23 20:05:32'], [['received_2018651381724765.gif'], 'received_2018651381724765.gif', '.gif', '446 KB', '2021.09.23 20:05:32'], [['Untitled-1.png'], 'Untitled-1.png', '.png', '4 674 KB', '2002.04.09 21:53:22'], [['Untitled-13.png'], 'Untitled-13.png', '.png', '4 601 KB', '2002.04.09 21:51:34'], [['Ushedshim slishkom rano.mp3'], 'Ushedshim slishkom rano.mp3', '.mp3', '5 236 KB', '2022.06.30 23:39:06'], [['Vesna.mp3'], 'Vesna.mp3', '.mp3', '7 226 KB', '2022.06.30 23:39:04'], [['Voda.mp3'], 'Voda.mp3', '.mp3', '5 532 KB', '2022.06.30 23:39:01'], [['WOL_MIESZKANIE 2020_14.skp'], 'WOL_MIESZKANIE 2020_14.skp', '.skp', '43 070 KB', '2022.06.02 09:06:42'], [['WOL_MODEL 1.skp'], 'WOL_MODEL 1.skp', '.skp', '25 108 KB', '2009.10.25 11:38:28'], [['ZAPROSZENIE.psd'], 'ZAPROSZENIE.psd', '.psd', '2 563 KB', '2011.04.14 22:46:34']]
        self.gap = "___ "

        uic.loadUi("GUI.ui", self)

        # Move main window to the center of the screen
        qtRectangle = self.frameGeometry()
        centerPiont = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPiont)
        self.move(qtRectangle.topLeft())

        self.central_widget = self.findChild(QWidget, "centralwidget")

        self.tree = self.findChild(QTreeWidget, "tree_A")

        self.tree_B = self.findChild(QTreeWidget, "tree_B")

        self.tree.itemDoubleClicked.connect(self.editItem)

        self.summary_label_A = self.findChild(QLabel, "label_A")

        # self.tree_from_dict(parent=self.tree, data=self.d)
        self.tree_from_list(data=self.ee)
        # self.print_tree(self.ee)



        # item = QTreeWidgetItem(self.tree, ['JEDYNKA'])
        # item = QTreeWidgetItem(self.tree, ['DWÓJKA'])
        # # item.setText(0, 'kot')
        # # item.setText(1, '1')
        # _111 = QTreeWidgetItem(item, ['111', 'bbb', 'fffff'])
        # bbb = QTreeWidgetItem(_111, ['bbbbb', 'b b b ', 'b'])
        # # _222 = QTreeWidgetItem(item, ['222', 'bbb', 'fffff'])
        # ccc = QTreeWidgetItem(_111, ['ccccc', 'c c c ', 'c'])
        # _333 = QTreeWidgetItem(item, ['333', 'bbb', 'fffff'])
        # ddd = QTreeWidgetItem(aaa, ['ddddd', 'd d d ', 'd'])
        # item = QTreeWidgetItem(item)
        # bbb.setText(0, 'pies')
        # aaa.setText(1, '2222')
        # item.setText(0, 'kot')
        # item.setText(1, '3')

        self.tree.expandAll()
        self.summary_label_A.setText(
            "{} files found".format(self.tree_A.topLevelItemCount()))
        self.show()

    def print_tree(self, data):
        path = ''
        old = ''

        for row in data:
            path_list = row[0]
            path = ''

            if old != path_list[-1]:
                for n in range(len(path_list)):
                    if n < len(path_list)-1:
                        path = path + "---" + path_list[n]

            print("PATH: ", path)

            if len(row) == 1:  # folder
                print(path + ".." + path_list[-1])
            else:  # plik
                print(path + "__" + path_list[-1] + "   obrazek")
                path = ''
            old = path_list[:-1]

    def tree_from_list(self, data=None):
        root = self.tree
        parent = root
        flag = ''
        folder = []

        for row in data:  # 'row' = Single file records
            path_list = row[0]  # file path as list of folders

            print("OLD: ", folder)
            print("PATH: ", path_list[:-1])
            if len(row[0]) == 1:
                parent = root

            if folder != path_list[:-1]:

                for item in path_list[:-1]:
                    if not (item in folder):
                        parent = QTreeWidgetItem(parent, [item])

                folder = path_list[:-1]


            if len(row) > 1:
                QTreeWidgetItem(parent, [path_list[-1]])  # Add file to tree





            # if old != path_list[-1]:  # if different from previous
            #     for n in range(len(path_list)):
            #         if n < len(path_list) - 1:
            #
            #     if old == path_list[:-1]:
            #        if flag != path_list[-2]:
            #
            #             flag = path_list[-2]
            # else:
            #     parent = root
            #
            # if len(row) > 1:  # file
            #
            # if len(row) == 1:  #folder
            #     old = path_list[-1]


    def tee(self, parent):
        root = QTreeWidgetItem(parent)
        titem = QTreeWidgetItem(root, ['Top'])
        child = QTreeWidgetItem(titem, ['pies','osioł'])
        child.setText(0, 'kot')
        # titemm = QTreeWidgetItem(titem)

        self.tree.expandAll()



            # item.setText(0, key)
            # l = [i for i in value[0].split("\\")]

    def tree_from_dict(self, data=None, parent=None):
        for key, value in data.items():
            item = QTreeWidgetItem(parent)

            item.setText(0, key)

            if isinstance(value, dict):
                self.tree_from_dict(data=value, parent=item)
            elif isinstance(value, list):
                [self.tree_from_dict(i, parent=item) for idx, i in enumerate(value)]
            else:
                item.setText(1, value)


    def editItem(self, item, column):

        try:
            if column == 1:
              item.setFlags(item.flags() | Qt.ItemIsEditable)
            else:
                pass
        except Exception as e:
            print(e)



    def save_changes(self):
        d = self.tree_2_dict(self.tree.invisibleRootItem())
        print(d)

    def tree_2_dict(self, parent, d=None):
        if d is None:
            d = {}
        for index in range(parent.childCount()):
            child = parent.child(index)
            if child.childCount():
                self.tree_2_dict(child, d.setdefault(child.text(0), {}))
            else:
                d[child.text(0)] = child.text(1)
        return d


app = QApplication(sys.argv)
UIWindow = MyWindow()
app.exec_()

# squares = []
# d = []
#
# for i in range(10):
# 	if i % 2 == 0:
# 		squares.append(i ** 2)
#
# print(squares)
# [0, 4, 16, 36, 64]

# gen = (i**2 for i in range(10) if i % 2 == 0)
#
# print(next(gen))
# print(next(gen))
# print(next(gen))
#
#
# a = [1, 2, 3, 4]
# b = []
# for x in a:
# 	b.append(x+1)
# print(b)
#
# print([x+1 for x in a])
#
# x = 50
#
# if x > 42:
# 	print("no")
# elif x == 42:
# 	print("yes")
# else:
# 	print("maybe")
#
# print("no") if x > 42 else print("Yes") if x == 42 else print("maybe")
#
# hi = 'hello world!'
# file = 'hello.txt'
# # Write hi in file
#
# s='s=%r;print(s%%s,sep="")';print(s%s,sep="")

# l = [4, 2, 1, 42, 3]
# print(sorted(l))
#
# l = [4, 2, 1, 42, 3]
# def sort(l):
# 	ll = []
# 	lr = []
# 	for i in range(len(l)):
# 		if i+1 < len(l):
# 			print(i+1, len(l))
# 			if l[i] >= l[i+1]:
# 				t = l[i+1]
# 				t2 = l[i]
# 				l[i] = t
# 				l[i+1] = t2
#
# 	return l, ll, lr
#
# print(sort(l))
# # print(lr, ll)
