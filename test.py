import exifread, time, os
import logging
from datetime import datetime as dt

path = "D:\TEMP\\IMG_4120.jpeg"

logging.basicConfig(level=logging.ERROR)
print(type(os.path.getmtime(path)), os.path.getmtime(path) )

def ts_to_dt(ts):
    return dt.fromtimestamp(ts)

def dateformat(date_string):
    date_string = date_string.strftime("%Y.%m.%d %H:%M:%S")
    return date_string

try:
    file = open(path, 'rb')  # opens file to check if EXIF tag is there with date of picture taken
    tags = exifread.process_file(file, stop_tag="EXIF DateTimeOriginal")
    date_t = str(tags["EXIF DateTimeOriginal"])  # Picture taken date
except:
    date_t = "Z"
    pass
else:
    date_t = date_t[:4] + "." + date_t[5:7] + "." + date_t[8:]
    print(type(date_t),date_t)

date_m = dateformat(ts_to_dt(os.path.getmtime(path)))  # Modification date
date_c = dateformat(ts_to_dt(os.path.getctime(path)))  # File creation date
dates = sorted([date_t, date_c, date_m])
print(dates)
print(dates[0])

# for tag in tags.keys():
#     if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#         print("Key: %s, value %s" % (tag, tags[tag]))

# def is_image(pict):
# 	file_type = os.path.splitext(pict)[1].upper()
# 	if file_type in [".jpg", ".tif", ".tiff", ".bmp", ".png", ".gif", ".raw", ".nef", ".jpeg", ".cr2",
# 	                                 ".orf", ".sr2", ".tga", "ciff", ".dng", ".wav", ".pcm", ".webp", ".dcf", ]:
# 		return file_type
# 	else:
# 		return False