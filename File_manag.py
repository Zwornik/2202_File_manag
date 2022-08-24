import exifread
import os
import logging
from datetime import datetime as dt
import tkinter as tk
from tkinter import filedialog
# from GUI_call import *

logging.basicConfig(level=logging.ERROR)
file_list = []

# Display dialog window asking for the folder
def folder_input():

	folder = input("Press 'Enter' to select a folder with your files: ")

	root = tk.Tk()
	root.wm_attributes('-topmost', True)  # Dialog window on top of other windows
	root.title("Centering windows")

	# Centering dialog window
	window_height = 800
	window_width = 800
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x_coordinate = int((screen_width / 2) - (window_width / 2))
	y_coordinate = int((screen_height / 2) - (window_height / 2))
	root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

	# Hiding root window
	root.overrideredirect(1)
	root.withdraw()

	folder = filedialog.askdirectory()  # Getting user input

	if folder == "":  # Terminates program if folder was not selected
		exit()
	root.destroy()  # kills dialog and root window
	folder = folder.replace("/", "\\")

	return folder


folder = folder_input()

date_extract = input('Do you want to extract the date when a picture was taken from the metadata of each file? \n'
					 'Selecting "YES" will make it much slower. (Y/N): ').upper()

sort_by = input("Sort files by...\nN - Name,  T - Type,  S - Size,  D - Date  >> ").upper()

c = 0


def ts_to_dt(ts):
	return dt.fromtimestamp(ts)


def dateformat(date_string):
	date_string = date_string.strftime("%Y.%m.%d %H:%M:%S")
	return date_string


# EXTRACTING 3 PICTURE CREATION DATE AND RETURNS THE OLDEST ONE

def oldest_date(path, date_extract):
	date_m = dateformat(ts_to_dt(os.path.getmtime(path)))  # Modification date
	date_c = dateformat(ts_to_dt(os.path.getctime(path)))  # File creation date

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


# Walking through all files in folder and subfolders
class Walk_folders():

	for path, subdirs, files in os.walk(folder):
		for item in os.scandir(path):
			if item.is_file():
				c += 1
				path = item.path
				date = oldest_date(path, date_extract)
				name = item.name
				file_type = os.path.splitext(item)[1]
				file_date = dateformat(ts_to_dt(item.stat().st_atime))
				size = ("{:,.0f}".format(item.stat().st_size / 1000).replace(",", " "))

				file_list.append((name, file_type, size, date, path))
				#print("{:<30s}   {}  {:>12} KB   {}   {}".format(name, file_type, size, date, path))

		print(type(name), type(file_type), type(size), type(file_date), type(date), type(path))
print(c)
print(file_list)


def display_file(file):
	return ("{:<30s}{}{:>12} KB    {:<60}".format(
			file.name, dateformat(ts_to_dt(file.stat().st_atime)), int(file.stat().st_size / 1000), file.path, )
	)

# EXIF data from picture reader
