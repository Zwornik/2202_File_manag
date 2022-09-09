import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Thread(QtCore.QThread):
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.runs = True
        self.path = "C:/TEMP"

    def run(self):
        self.walk(self.path)
        self.stop()
        self.finished.emit()   # this one is not even necessary

    def stop(self):
        self.runs = False

    # def commence_working(self):
    def walk(self, path):
        with os.scandir(path) as folder:
            for item in folder:
                if self.runs:
                    for i in range(1):
                        time.sleep(0.5)
                    if item.is_dir():
                        path = item.path
                        print("path: ", path)
                        self.walk(path)
                    elif item.is_file:
                        print(item.path)



class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.l = QLabel("Hello World", self)

        self.b = QPushButton(self)
        self.b.setText("abort thread")

        self.sb = QPushButton(self)
        self.sb.setText("start thread")

        self.vb = QHBoxLayout()
        self.vb.addWidget(self.l)
        self.vb.addWidget(self.b)
        self.vb.addWidget(self.sb)
        self.setLayout(self.vb)

        self.b.clicked.connect(self.on_userAbort_clicked)
        self.sb.clicked.connect(self.start_thread_clicked)

    def on_userAbort_clicked(self):
        self.l.setText("aborting the thread...")
        self.thread.stop()
        self.thread.wait()

    def start_thread_clicked(self):
        self.thread = Thread()
        self.thread.finished.connect(self.thread_finished)
        self.l.setText("The thread is running")
        self.thread.start()

    def thread_finished(self):
            self.l.setText("The thread stopped")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    g = GUI()
    g.show()
    sys.exit(app.exec_())




# sub_yes = True
# walk(path, sub_yes)

