import exifread
import os
import time
import scandir
from datetime import datetime as dt

# fdir = input("Specify first folder: ")
folder = "D:\TEMP"
c = 0

def ts_to_dt(ts):
	return dt.fromtimestamp(ts)


def dateformat(date_string):
	date_string = date_string.strftime("%Y.%m.%d  %H:%M:%S.%f")
	return date_string[:-4]

for path, subdirs, files in os.walk(folder):
	for item in os.scandir(path):
		if item.is_file():
			c += 1
			# if extension in
			with open(item, 'rb') as file:
				tags = exifread.process_file(file, stop_tag="EXIF DateTimeOriginal")
				try:
					tags["EXIF DateTimeOriginal"] == True
				except:
					print("Błąd")
				else:
					taken = tags["EXIF DateTimeOriginal"]

			print("{:<30s}   {}   {}{:>12,} KB   {}   {:<60}".format(
			item.name, os.path.splitext(item)[1], dateformat(ts_to_dt(item.stat().st_atime)),
				(item.stat().st_size / 1000).replace(","," ") , taken, item.path,
				))

print(c)
def display_file(file):
	return ("{:<30s}{}{:>12} KB    {:<60}".format(
		file.name, dateformat(ts_to_dt(file.stat().st_atime)), int(file.stat().st_size / 1000), file.path, )
	)

print("last modified: %s" % time.ctime(os.path.getmtime("D:\TEMP\\20160130_215245.jpg")))
print("created: %s" % time.ctime(os.path.getctime("D:\TEMP\\20160130_215245.jpg")))

# EXIF data from picture reader

